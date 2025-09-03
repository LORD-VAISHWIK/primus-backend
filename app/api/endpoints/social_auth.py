from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
import os
from starlette.config import Config
from app.models import User
from app.database import SessionLocal
from app.schemas import UserOut
from jose import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests

router = APIRouter()

config = Config('.env')

oauth = OAuth(config)

# Register providers
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v3/',
    client_kwargs={'scope': 'openid email profile'}
)
oauth.register(
    name='discord',
    client_id=os.getenv("DISCORD_CLIENT_ID"),
    client_secret=os.getenv("DISCORD_CLIENT_SECRET"),
    access_token_url='https://discord.com/api/oauth2/token',
    authorize_url='https://discord.com/api/oauth2/authorize',
    api_base_url='https://discord.com/api/',
    client_kwargs={'scope': 'identify email'}
)
oauth.register(
    name='twitter',
    client_id=os.getenv("TWITTER_CLIENT_ID"),
    client_secret=os.getenv("TWITTER_CLIENT_SECRET"),
    request_token_url='https://api.twitter.com/oauth/request_token',
    request_token_params=None,
    access_token_url='https://api.twitter.com/oauth/access_token',
    access_token_params=None,
    authorize_url='https://api.twitter.com/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.twitter.com/1.1/',
    client_kwargs=None
)
# Apple OAuth requires more advanced setup; recommend starting with Google/Discord/Twitter.

# Helper to get or create user
def get_or_create_user(db, email, username, provider):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    # Create new user
    user = User(
        name=username or email.split('@')[0],
        email=email,
        password_hash="oauth",  # mark as social login
        role="client",
        is_email_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_access_token(data: dict):
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretjwtkey")
    ALGORITHM = "HS256"
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.get("/login/{provider}")
async def oauth_login(request: Request, provider: str, state: str | None = None):
    redirect_uri = request.url_for('auth_callback', provider=provider)
    client = oauth.create_client(provider)
    # Basic sanity for Google credentials to avoid 500s
    if provider == 'google':
        cid = os.getenv("GOOGLE_CLIENT_ID")
        csec = os.getenv("GOOGLE_CLIENT_SECRET")
        if not cid or not csec:
            raise HTTPException(400, "Google OAuth not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET, and add redirect URI /api/social/auth/google in Google Cloud Console.")
    try:
        # Pass state through so we can redirect back to a custom return URL in the callback
        return await client.authorize_redirect(request, redirect_uri, state=state)
    except Exception as e:
        raise HTTPException(400, f"OAuth init failed: {e}")

@router.get("/auth/{provider}")
async def auth_callback(request: Request, provider: str):
    db = SessionLocal()
    try:
        token = await oauth.create_client(provider).authorize_access_token(request)
        if provider == "google":
            userinfo = await oauth.google.parse_id_token(request, token)
            email = userinfo['email']
            username = userinfo.get('name') or userinfo['email'].split('@')[0]
        elif provider == "discord":
            resp = await oauth.discord.get('users/@me', token=token)
            profile = resp.json()
            email = profile["email"]
            username = profile["username"]
        elif provider == "twitter":
            # Twitter returns in a different way; see docs for details.
            # Simplified for demonstration:
            resp = await oauth.twitter.get('account/verify_credentials.json?include_email=true', token=token)
            profile = resp.json()
            email = profile.get("email")  # Twitter API may restrict email
            username = profile["screen_name"]
        else:
            raise HTTPException(400, "Provider not supported yet.")
        user = get_or_create_user(db, email, username, provider)
        access_token = create_access_token({"sub": user.email, "role": user.role})
        state = request.query_params.get("state")
        if state and (state.startswith("http://127.0.0.1") or state.startswith("http://localhost")):
            # Redirect back to desktop listener with token for local capture
            return RedirectResponse(url=f"{state}?token={access_token}")
        # Fallback: return token JSON
        return {"access_token": access_token, "token_type": "bearer"}
    except OAuthError as err:
        raise HTTPException(400, f"OAuth error: {err}")


class GoogleIdTokenIn(BaseModel):
    id_token: str
    client_id: str | None = None


@router.post("/google/idtoken")
def login_with_google_idtoken(payload: GoogleIdTokenIn):
    db = SessionLocal()
    try:
        audience = payload.client_id or os.getenv("GOOGLE_CLIENT_ID") or "496813374696-q63fi7dr27q34hvgk6d8tolsv8rtitdg.apps.googleusercontent.com"
        claims = google_id_token.verify_oauth2_token(payload.id_token, google_requests.Request(), audience)
        email = claims.get("email")
        if not email:
            raise HTTPException(400, "Google token missing email")
        username = claims.get("name") or email.split('@')[0]
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                name=username,
                email=email,
                password_hash="oauth",
                role="client",
                is_email_verified=bool(claims.get("email_verified", True)),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        access_token = create_access_token({"sub": user.email, "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(400, "Invalid Google token")
    finally:
        db.close()
