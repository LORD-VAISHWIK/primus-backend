import os
import firebase_admin
from firebase_admin import auth as fb_auth, credentials as fb_credentials

_INITIALIZED = False


def ensure_initialized() -> None:
    global _INITIALIZED
    if _INITIALIZED and firebase_admin._apps:
        return
    cred_path = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if not cred_path:
        raise RuntimeError("FIREBASE_CREDENTIALS_JSON is not set")
    if not firebase_admin._apps:
        cred = fb_credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    _INITIALIZED = True


def verify_id_token(id_token: str) -> dict:
    ensure_initialized()
    return fb_auth.verify_id_token(id_token)


