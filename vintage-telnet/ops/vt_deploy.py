#!/usr/bin/env python3
"""Despliegue reusable y transaccional de Vintage Telnet en Raspberry Pi."""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import pwd
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

DEFAULT_REPO_ROOT = Path('/home/jdiaz/MatiasGameLab')
INSTALL_ROOT = Path('/opt/vintage-telnet')
RELEASES_ROOT = INSTALL_ROOT / 'releases'
CURRENT_LINK = INSTALL_ROOT / 'current'
DATA_DIR = Path('/var/lib/vintage-telnet')
DATABASE = DATA_DIR / 'vintage.sqlite3'
BACKUP_DIR = Path('/var/backups/vintage-telnet')
SERVICE = 'vintage-telnet.service'
BACKUP_SERVICE = 'vintage-telnet-backup.service'
LOCK_FILE = Path('/run/lock/vintage-telnet-deploy.lock')
LOCAL_HEALTH = 'http://127.0.0.1:8080/healthz'
EXTERNAL_HEALTH = 'https://raspberrypi.tail3d212e.ts.net/healthz'

class DeployError(RuntimeError):
    pass

def log(message: str) -> None:
    print(f'[vt-deploy] {message}', flush=True)

def run(cmd: list[str], *, cwd: Path | None = None, timeout: int = 300,
        capture: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    log('$ ' + ' '.join(cmd))
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True,
                          stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.STDOUT if capture else None,
                          timeout=timeout, check=False)
    if check and proc.returncode != 0:
        detail = f"\n{proc.stdout.strip()}" if capture and proc.stdout else ''
        raise DeployError(f"Falló ({proc.returncode}): {' '.join(cmd)}{detail}")
    return proc

def git_command(repo_owner: str, repo_owner_home: str, *args: str) -> list[str]:
    # Ejecutar Git como dueño del checkout evita dubious ownership, conserva
    # sus credenciales/config de GitHub y no deja archivos root-owned en el repo.
    return ['runuser', '-u', repo_owner, '--', 'env', f'HOME={repo_owner_home}', 'git', *args]

def git_output(repo: Path, repo_owner: str, repo_owner_home: str, *args: str) -> str:
    proc = run(git_command(repo_owner, repo_owner_home, *args), cwd=repo, capture=True)
    return (proc.stdout or '').strip()

def resolve_authorized_sha(repo: Path, repo_owner: str, repo_owner_home: str, revision: str, *, skip_fetch: bool) -> str:
    if not skip_fetch:
        run(git_command(repo_owner, repo_owner_home, 'fetch', '--prune', 'origin'), cwd=repo, timeout=180)
    requested = 'origin/main' if revision in ('main', 'latest') else revision
    sha = git_output(repo, repo_owner, repo_owner_home, 'rev-parse', '--verify', f'{requested}^{{commit}}')
    if len(sha) != 40:
        raise DeployError(f'No se pudo resolver un SHA completo para {revision!r}.')
    proc = run(git_command(repo_owner, repo_owner_home, 'merge-base', '--is-ancestor', sha, 'origin/main'),
               cwd=repo, capture=True, check=False)
    if proc.returncode != 0:
        raise DeployError(f'{sha} no es ancestro de origin/main. Integra la entrega antes de desplegar.')
    return sha

def archive_commit(repo: Path, repo_owner: str, repo_owner_home: str, sha: str, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    git = subprocess.Popen(git_command(repo_owner, repo_owner_home, 'archive', '--format=tar', sha),
                           cwd=str(repo), stdout=subprocess.PIPE)
    assert git.stdout is not None
    tar = subprocess.run(['tar', '-xf', '-', '-C', str(destination)], stdin=git.stdout, check=False)
    git.stdout.close()
    git_rc = git.wait()
    if git_rc != 0 or tar.returncode != 0:
        raise DeployError(f'No se pudo crear el release (git archive={git_rc}, tar={tar.returncode}).')

def read_expected_schema(project: Path) -> int:
    proc = run([str(project / '.venv/bin/python'), '-c',
                'from server.store import SCHEMA_VERSION; print(SCHEMA_VERSION)'],
               cwd=project, capture=True)
    try:
        return int((proc.stdout or '').strip().splitlines()[-1])
    except (ValueError, IndexError) as exc:
        raise DeployError('No se pudo leer SCHEMA_VERSION del release.') from exc

def database_player_ids(db_path: Path) -> list[str]:
    if not db_path.exists():
        raise DeployError(f'No existe la base viva: {db_path}')
    uri = db_path.resolve().as_uri() + '?mode=ro'
    db = sqlite3.connect(uri, uri=True)
    try:
        return [str(row[0]) for row in db.execute('SELECT id FROM players ORDER BY id')]
    finally:
        db.close()

def newest_backup() -> Path:
    files = sorted(BACKUP_DIR.glob('vintage-*.sqlite3'),
                   key=lambda p: p.stat().st_mtime_ns, reverse=True)
    if not files:
        raise DeployError('El servicio de backup no produjo ningún vintage-*.sqlite3.')
    return files[0]

def verified_backup() -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    before = {p.resolve(): p.stat().st_mtime_ns for p in BACKUP_DIR.glob('vintage-*.sqlite3')}
    run(['systemctl', 'reset-failed', BACKUP_SERVICE], check=False)
    run(['systemctl', 'start', BACKUP_SERVICE], timeout=120)
    result = run(['systemctl', 'show', BACKUP_SERVICE, '-p', 'Result', '--value'], capture=True).stdout
    if (result or '').strip() != 'success':
        raise DeployError(f'{BACKUP_SERVICE} no terminó en success: {(result or "").strip()}')
    backup = newest_backup()
    previous_mtime = before.get(backup.resolve())
    if previous_mtime is not None and previous_mtime == backup.stat().st_mtime_ns:
        raise DeployError('No se detectó un backup nuevo en esta ejecución.')
    return backup

def validate_migration_on_copy(project: Path, backup: Path, expected_schema: int) -> None:
    with tempfile.TemporaryDirectory(prefix='vt-migration-') as tmp:
        tmpdir = Path(tmp)
        test_db = tmpdir / 'vintage.sqlite3'
        shutil.copy2(backup, test_db)
        code = ('from server import store; '
                f'store.initialize({str(test_db)!r}); '
                f'assert store.SCHEMA_VERSION == {expected_schema}')
        run([str(project / '.venv/bin/python'), '-c', code], cwd=project, timeout=120)
        proc = run([str(project / '.venv/bin/python'), '-m', 'server.admin',
                    '--data-dir', str(tmpdir), 'check'], cwd=project, capture=True, timeout=120)
        payload = json.loads((proc.stdout or '').strip().splitlines()[-1])
        if payload.get('schema_version') != expected_schema:
            raise DeployError(
                f"La migración de ensayo terminó con schema {payload.get('schema_version')} "
                f"en vez de {expected_schema}."
            )

def atomic_current(target: Path) -> None:
    next_link = INSTALL_ROOT / f'.current-next-{os.getpid()}'
    try:
        next_link.unlink(missing_ok=True)
        next_link.symlink_to(target)
        os.replace(next_link, CURRENT_LINK)
    finally:
        next_link.unlink(missing_ok=True)

def health_payload(timeout_seconds: int = 35) -> dict:
    deadline = time.monotonic() + timeout_seconds
    last_error = ''
    while time.monotonic() < deadline:
        try:
            req = urllib.request.Request(
                LOCAL_HEALTH,
                headers={'Accept': 'application/json', 'User-Agent': 'vt-deploy/1'},
            )
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    return json.loads(response.read().decode('utf-8'))
                last_error = f'HTTP {response.status}'
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            last_error = str(exc)
        time.sleep(1)
    raise DeployError(f'/healthz no quedó listo: {last_error}')

def external_health_info() -> None:
    try:
        req = urllib.request.Request(
            EXTERNAL_HEALTH,
            headers={'Accept': 'application/json', 'User-Agent': 'vt-deploy/1'},
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            body = response.read().decode('utf-8', errors='replace')
            log(f'Funnel informativo: HTTP {response.status} {body[:180]}')
    except Exception as exc:
        log(f'AVISO: no se pudo validar Funnel; no revierte producción local: {exc}')

def restore_database(backup: Path, original_stat: os.stat_result) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp = DATA_DIR / f'.vintage-rollback-{os.getpid()}.sqlite3'
    try:
        shutil.copy2(backup, tmp)
        os.chown(tmp, original_stat.st_uid, original_stat.st_gid)
        os.chmod(tmp, original_stat.st_mode & 0o777)
        os.replace(tmp, DATABASE)
        for suffix in ('-wal', '-shm'):
            Path(str(DATABASE) + suffix).unlink(missing_ok=True)
    finally:
        tmp.unlink(missing_ok=True)

def rollback(previous_target: Path | None, backup: Path, original_stat: os.stat_result) -> None:
    log('FALLO POST-SWITCH: iniciando rollback automático.')
    run(['systemctl', 'stop', SERVICE], check=False, timeout=60)
    restore_database(backup, original_stat)
    if previous_target is not None:
        atomic_current(previous_target)
        run(['systemctl', 'start', SERVICE], timeout=60)
        try:
            payload = health_payload()
            log(f'Rollback recuperó servicio: {payload}')
        except DeployError as exc:
            log(f'ALERTA: rollback restauró código/base pero health sigue fallando: {exc}')
    else:
        log('ALERTA: no había release previo; base restaurada y servicio quedó detenido.')

def main() -> int:
    parser = argparse.ArgumentParser(
        description='Despliega un SHA de main de Vintage Telnet con backup, tests y rollback.'
    )
    parser.add_argument('revision', help='SHA completo/prefijo o ref ya integrado a origin/main.')
    parser.add_argument(
        '--repo-root',
        type=Path,
        default=Path(os.environ.get('VT_REPO_ROOT', str(DEFAULT_REPO_ROOT))),
    )
    parser.add_argument(
        '--skip-fetch',
        action='store_true',
        help='No hace git fetch; solo si origin/main ya está actualizado localmente.',
    )
    args = parser.parse_args()

    if os.geteuid() != 0:
        raise DeployError('Ejecuta este comando con sudo.')

    repo = args.repo_root.resolve()
    if not (repo / '.git').exists():
        raise DeployError(f'No es un checkout Git válido: {repo}')
    if not (repo / 'vintage-telnet').is_dir():
        raise DeployError(f'Falta vintage-telnet/ en {repo}')

    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOCK_FILE.open('w') as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise DeployError('Ya hay otro vt-deploy en ejecución.') from exc

        owner_entry = pwd.getpwuid(repo.stat().st_uid)
        repo_owner = owner_entry.pw_name
        repo_owner_home = owner_entry.pw_dir
        sha = resolve_authorized_sha(
            repo, repo_owner, repo_owner_home, args.revision, skip_fetch=args.skip_fetch
        )
        log(f'SHA autorizado: {sha}')

        current_target: Path | None = None
        if CURRENT_LINK.exists() or CURRENT_LINK.is_symlink():
            current_target = CURRENT_LINK.resolve()
            if current_target.name == sha:
                payload = health_payload()
                log(f'Ya está desplegado {sha}; health={payload}. No se hizo ningún cambio.')
                return 0

        RELEASES_ROOT.mkdir(parents=True, exist_ok=True)
        final_release = RELEASES_ROOT / sha
        if final_release.exists():
            raise DeployError(
                f'El release {final_release} ya existe pero no es current. '
                'Revísalo manualmente antes de reutilizarlo.'
            )

        stage = Path(tempfile.mkdtemp(prefix=f'.{sha[:12]}-', dir=RELEASES_ROOT))
        backup: Path | None = None
        switched = False
        original_stat = DATABASE.stat() if DATABASE.exists() else None

        try:
            log('Preparando release aislado.')
            stage.rmdir()
            archive_commit(repo, repo_owner, repo_owner_home, sha, stage)
            project = stage / 'vintage-telnet'
            if not project.is_dir():
                raise DeployError('El archive no contiene vintage-telnet/.')

            run(['python3', '-m', 'venv', str(project / '.venv')], timeout=120)
            run(
                [
                    str(project / '.venv/bin/pip'),
                    'install',
                    '--disable-pip-version-check',
                    '-r',
                    str(project / 'requirements.txt'),
                ],
                cwd=project,
                timeout=300,
            )
            run(
                [
                    str(project / '.venv/bin/python'),
                    '-m',
                    'unittest',
                    'discover',
                    '-s',
                    'tests',
                    '-v',
                ],
                cwd=project,
                timeout=300,
            )
            expected_schema = read_expected_schema(project)
            log(f'Schema esperado leído del release: {expected_schema}')

            before_players = database_player_ids(DATABASE)
            log(f'Jugadores antes del deploy: {len(before_players)}')

            backup = verified_backup()
            log(f'Backup previo verificado: {backup}')
            validate_migration_on_copy(project, backup, expected_schema)
            log('Migración validada contra una copia del backup.')

            (stage / '.vt-release-sha').write_text(sha + '\n', encoding='utf-8')
            os.replace(stage, final_release)
            project = final_release / 'vintage-telnet'

            run(['systemctl', 'stop', SERVICE], timeout=60)
            atomic_current(final_release)
            switched = True
            run(['systemctl', 'start', SERVICE], timeout=60)

            payload = health_payload()
            if payload.get('status') != 'ok':
                raise DeployError(f'healthz no reporta status=ok: {payload}')
            try:
                live_schema = int(payload.get('schema_version', -1))
            except (TypeError, ValueError) as exc:
                raise DeployError(f'healthz devolvió schema inválido: {payload}') from exc
            if live_schema != expected_schema:
                raise DeployError(
                    f'healthz reporta schema {live_schema} pero release espera {expected_schema}.'
                )

            after_players = database_player_ids(DATABASE)
            if after_players != before_players:
                raise DeployError('La lista de IDs de jugadores cambió durante el despliegue.')

            run(
                [
                    str(project / '.venv/bin/python'),
                    str(project / 'ops/raspberry_preflight.py'),
                    '--expected-head',
                    sha,
                    '--skip-external',
                ],
                cwd=project,
                timeout=180,
            )

            log(
                f'DESPLIEGUE OK: {sha} · schema {expected_schema} · '
                f'{len(after_players)} jugadores preservados.'
            )
            external_health_info()
            log('Backup diario permanece a cargo de vintage-telnet-backup.timer.')
            return 0

        except Exception:
            if switched and backup is not None and original_stat is not None:
                rollback(current_target, backup, original_stat)
            raise
        finally:
            if stage.exists():
                shutil.rmtree(stage, ignore_errors=True)

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except DeployError as exc:
        print(f'[vt-deploy] ERROR: {exc}', file=sys.stderr)
        raise SystemExit(1)
