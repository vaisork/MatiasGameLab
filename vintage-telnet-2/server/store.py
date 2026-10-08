"""Transactional persistence for the new world."""
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

SCHEMA = '''
CREATE TABLE IF NOT EXISTS accounts(id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS account_access(account_id INTEGER PRIMARY KEY REFERENCES accounts(id), blocked INTEGER NOT NULL DEFAULT 0, session_version INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS characters(id INTEGER PRIMARY KEY, account_id INTEGER NOT NULL REFERENCES accounts(id), name TEXT NOT NULL, species TEXT NOT NULL, class_id TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'pending', state TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS world(id INTEGER PRIMARY KEY CHECK(id=1), state TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS requests(character_id INTEGER NOT NULL, request_id TEXT NOT NULL, intent TEXT NOT NULL, result TEXT NOT NULL, PRIMARY KEY(character_id,request_id));
CREATE TABLE IF NOT EXISTS approvals(character_id INTEGER PRIMARY KEY, approved_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS dm_requests(character_id INTEGER NOT NULL, request_id TEXT NOT NULL, intent TEXT NOT NULL, metadata TEXT NOT NULL, PRIMARY KEY(character_id,request_id));
CREATE TABLE IF NOT EXISTS dm_grants(id INTEGER PRIMARY KEY, character_id INTEGER NOT NULL, item_id TEXT NOT NULL, amount INTEGER NOT NULL, removed INTEGER NOT NULL DEFAULT 0, baseline INTEGER NOT NULL, instances TEXT NOT NULL, at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY, actor TEXT NOT NULL, action TEXT NOT NULL, target TEXT NOT NULL, at REAL NOT NULL);
'''

class Store:
    def __init__(self, path):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self.transaction() as db:
            db.executescript(SCHEMA)
            db.execute('INSERT OR IGNORE INTO world VALUES(1,?)', (json.dumps({'version':0,'flags':[],'deaths':{},'weather':{}}),))

    @contextmanager
    def transaction(self):
        db = sqlite3.connect(self.path, timeout=15)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        try:
            db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def load(row):
        if row is None:
            return None
        result = dict(row)
        result['state'] = json.loads(result['state'])
        return result

    @staticmethod
    def save(db, character):
        db.execute('UPDATE characters SET status=?,state=? WHERE id=?', (character['status'], json.dumps(character['state'], ensure_ascii=False), character['id']))

    @staticmethod
    def world(db):
        return json.loads(db.execute('SELECT state FROM world WHERE id=1').fetchone()[0])

    @staticmethod
    def save_world(db, state):
        state['version'] += 1
        db.execute('UPDATE world SET state=? WHERE id=1', (json.dumps(state, ensure_ascii=False),))
