"""Dungeon Master authentication: one shared secret from VT_DM_PASSWORD.

No hay cuentas de DM separadas porque hoy solo Javier (Vaisork) ejerce ese
rol. Si eso cambia, esto deberia evolucionar a cuentas propias. Si
VT_DM_PASSWORD no esta configurada, el panel del DM queda deshabilitado
(falla cerrado) en vez de aceptar cualquier contrasena.
"""
import hmac
import os


def is_configured():
    return bool(os.environ.get("VT_DM_PASSWORD"))


def check_secret(candidate):
    expected = os.environ.get("VT_DM_PASSWORD")
    if not expected or not isinstance(candidate, str):
        return False
    return hmac.compare_digest(expected, candidate)
