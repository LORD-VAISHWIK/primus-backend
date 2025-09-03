from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
from app.api.endpoints import wallet
from app.database import engine, Base
from app.api.endpoints import auth, pc, session
from app.api.endpoints import game
from app.api.endpoints import remote_command
from app.api.endpoints import stats
from app.api.endpoints import chat, notification
from app.api.endpoints import support_ticket
from app.api.endpoints import announcement
from app.api.endpoints import hardware
from app.api.endpoints import update
from app.api.endpoints import audit
from app.api.endpoints import pc_ban
from app.api.endpoints import pc_group
from app.api.endpoints import backup
from app.api.endpoints import billing
from app.api.endpoints import webhook
from app.api.endpoints import social_auth
from app.api.endpoints import membership
from app.api.endpoints import booking
from app.api.endpoints import screenshot
from app.api.endpoints import pc_admin
from app.api.endpoints import cafe
from app.api.endpoints import license
from app.api.endpoints import client_pc
from app.api.endpoints import staff
from app.api.endpoints import offer
from app.api.endpoints import user_group
from app.api.endpoints import payment
from app.api.endpoints import prize
from app.api.endpoints import user
from app.api.endpoints import leaderboard
from app.api.endpoints import event
from app.api.endpoints import coupon
from app.api.endpoints import settings, games
from app.ws import pc as ws_pc
from app.ws import admin as ws_admin

# Load environment from .env if present
try:
    load_dotenv()
except Exception:
    pass

Base.metadata.create_all(bind=engine)

# Lightweight migration for SQLite: ensure users.wallet_balance column exists
# NOTE: This migration code is SQLite-specific using PRAGMA commands.
# For PostgreSQL production deployments, use Alembic for proper database migrations.
# The try-except block will safely skip this for non-SQLite databases.
try:
    from sqlalchemy import text
    with engine.connect() as conn:
        # Users
        res = conn.execute(text("PRAGMA table_info(users)"))
        cols = [row[1] for row in res]
        if 'wallet_balance' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN wallet_balance FLOAT DEFAULT 0.0"))
            conn.commit()
        if 'coins_balance' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN coins_balance INTEGER DEFAULT 0"))
            conn.commit()
        if 'user_group_id' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN user_group_id INTEGER"))
            conn.commit()
        if 'birthdate' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN birthdate DATETIME"))
            conn.commit()
        if 'two_factor_secret' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN two_factor_secret TEXT"))
            conn.commit()
        if 'is_email_verified' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_email_verified BOOLEAN DEFAULT 0"))
            conn.commit()
        if 'email_verification_sent_at' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN email_verification_sent_at DATETIME"))
            conn.commit()
        if 'first_name' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN first_name TEXT"))
            conn.commit()
        if 'last_name' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN last_name TEXT"))
            conn.commit()
        if 'phone' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN phone TEXT"))
            conn.commit()
        if 'tos_accepted' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN tos_accepted BOOLEAN DEFAULT 0"))
            conn.commit()
        if 'tos_accepted_at' not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN tos_accepted_at DATETIME"))
            conn.commit()
        # Games
        resg = conn.execute(text("PRAGMA table_info(games)"))
        gcols = [r[1] for r in resg]
        if 'min_age' not in gcols:
            conn.execute(text("ALTER TABLE games ADD COLUMN min_age INTEGER"))
            conn.commit()
        # Ensure new tables exist
        Base.metadata.create_all(bind=engine)
        # ClientPC migration: add current_user_id if missing
        resc = conn.execute(text("PRAGMA table_info(client_pcs)"))
        ccols = [r[1] for r in resc]
        if 'current_user_id' not in ccols:
            conn.execute(text("ALTER TABLE client_pcs ADD COLUMN current_user_id INTEGER"))
            conn.commit()
        if 'device_id' not in ccols:
            conn.execute(text("ALTER TABLE client_pcs ADD COLUMN device_id TEXT"))
            conn.commit()
        if 'bound' not in ccols:
            conn.execute(text("ALTER TABLE client_pcs ADD COLUMN bound BOOLEAN DEFAULT 0"))
            conn.commit()
        if 'bound_at' not in ccols:
            conn.execute(text("ALTER TABLE client_pcs ADD COLUMN bound_at DATETIME"))
            conn.commit()
        if 'grace_until' not in ccols:
            conn.execute(text("ALTER TABLE client_pcs ADD COLUMN grace_until DATETIME"))
            conn.commit()
        if 'suspended' not in ccols:
            conn.execute(text("ALTER TABLE client_pcs ADD COLUMN suspended BOOLEAN DEFAULT 0"))
            conn.commit()
        # Ensure challenges and tokens tables exist via ORM metadata
        Base.metadata.create_all(bind=engine)
except Exception:
    pass

app = FastAPI()

# CORS configuration
origins = [
    "https://primustech.in",     # Production frontend
    "https://www.primustech.in", # Production frontend (www)
    "http://localhost:5173",      # Vite dev server
    "http://localhost:3000",      # Alternative dev port
]

# FOR DEVELOPMENT ONLY: allow all origins when ALLOW_ALL_CORS=true
if os.getenv("ALLOW_ALL_CORS", "false").lower() == "true":
    # When allow_credentials=True, Starlette disallows wildcard origins; use regex instead
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(pc.router, prefix="/api/pc", tags=["pc"])
app.include_router(session.router, prefix="/api/session", tags=["session"])
app.include_router(wallet.router, prefix="/api/wallet", tags=["wallet"])
app.include_router(game.router, prefix="/api/game", tags=["game"])
app.include_router(remote_command.router, prefix="/api/command", tags=["remote_command"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(notification.router, prefix="/api/notification", tags=["notification"])
app.include_router(support_ticket.router, prefix="/api/support", tags=["support"])
app.include_router(announcement.router, prefix="/api/announcement", tags=["announcement"])
app.include_router(hardware.router, prefix="/api/hardware", tags=["hardware"])
app.include_router(update.router, prefix="/api/update", tags=["update"])
app.include_router(license.router, prefix="/api/license", tags=["license"])
app.include_router(audit.router, prefix="/api/audit", tags=["audit"])
app.include_router(pc_ban.router, prefix="/api/pcban", tags=["pcban"])
app.include_router(pc_group.router, prefix="/api/pcgroup", tags=["pcgroup"])
app.include_router(backup.router, prefix="/api/backup", tags=["backup"])
app.include_router(billing.router, prefix="/api/billing", tags=["billing"])
app.include_router(webhook.router, prefix="/api/webhook", tags=["webhook"])
app.include_router(social_auth.router, prefix="/api/social", tags=["social"])
app.include_router(membership.router, prefix="/api/membership", tags=["membership"])
app.include_router(booking.router, prefix="/api/booking", tags=["booking"])
app.include_router(screenshot.router, prefix="/api/screenshot", tags=["screenshot"])
app.include_router(pc_admin.router, prefix="/api/pcadmin", tags=["pcadmin"])
app.include_router(cafe.router, prefix="/api/cafe", tags=["cafe"])
# license router already included above
app.include_router(client_pc.router, prefix="/api/clientpc", tags=["clientpc"])
app.include_router(staff.router, prefix="/api/staff", tags=["staff"])
app.include_router(offer.router, prefix="/api/offer", tags=["offer"]) 
app.include_router(user_group.router, prefix="/api/usergroup", tags=["usergroup"]) 
app.include_router(payment.router, prefix="/api/payment", tags=["payment"]) 
app.include_router(prize.router, prefix="/api/prize", tags=["prize"]) 
app.include_router(user.router, prefix="/api/user", tags=["user"]) 
app.include_router(leaderboard.router, prefix="/api/leaderboard", tags=["leaderboard"]) 
app.include_router(event.router, prefix="/api/event", tags=["event"]) 
app.include_router(coupon.router, prefix="/api/coupon", tags=["coupon"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])
app.include_router(games.router, prefix="/api/games", tags=["games"]) 

# WebSocket routes
app.include_router(ws_pc.router)
app.include_router(ws_admin.router)


@app.get("/")
def root():
    return {"message": "Lance Backend Running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "ok",
        "service": "lance-backend",
        "timestamp": datetime.utcnow().isoformat()
    }

# Background task: periodically broadcast time-left hints to all connected PCs
import asyncio
import json
from app.database import SessionLocal
from app.models import ClientPC, User, PCToGroup, PricingRule, UserGroup, UserOffer
from datetime import datetime

_last_time_warn: dict[int, int] = {}

def _compute_minutes_for_pc(db, pc_id: int) -> int:
    # Map to pricing rule
    group_map = db.query(PCToGroup).filter_by(pc_id=pc_id).first()
    group_id = group_map.group_id if group_map else None
    now = datetime.utcnow()
    rule = db.query(PricingRule).filter(
        PricingRule.is_active == True,
        ((PricingRule.group_id == group_id) | (PricingRule.group_id == None)),
        ((PricingRule.start_time == None) | (PricingRule.start_time <= now)),
        ((PricingRule.end_time == None) | (PricingRule.end_time >= now)),
    ).order_by(PricingRule.group_id.desc()).first()
    if not rule:
        return 0
    cpc = db.query(ClientPC).filter_by(id=pc_id).first()
    if not cpc or not cpc.current_user_id:
        return 0
    user = db.query(User).filter_by(id=cpc.current_user_id).first()
    if not user:
        return 0
    rate = rule.rate_per_hour
    if getattr(user, 'user_group_id', None):
        ug = db.query(UserGroup).filter_by(id=user.user_group_id).first()
        if ug and ug.discount_percent:
            rate = rate * max(0.0, (100.0 - ug.discount_percent)) / 100.0
    offers = db.query(UserOffer).filter_by(user_id=user.id).all()
    offer_hours = sum(max(0.0, uo.hours_remaining or 0.0) for uo in offers)
    wallet_hours = 0.0
    if rate and rate > 0:
        wallet_hours = max(0.0, (user.wallet_balance or 0.0) / rate)
    total_minutes = int(round((offer_hours + wallet_hours) * 60))
    return total_minutes

async def _broadcast_timeleft_loop():
    while True:
        try:
            db = SessionLocal()
            try:
                # naive strategy: for each online client pc, compute using its current_user if set
                pcs = db.query(ClientPC).all()
                for pc in pcs:
                    minutes = 0
                    try:
                        minutes = _compute_minutes_for_pc(db, pc.id)
                    except Exception:
                        minutes = 0
                    last = _last_time_warn.get(pc.id)
                    # 5-minute warning
                    if minutes == 5 and last != 5:
                        try:
                            await ws_pc.notify_pc(pc.id, json.dumps({"type": "timeleft", "minutes": 5}))
                        except Exception:
                            pass
                        _last_time_warn[pc.id] = 5
                    # 1-minute final warning
                    elif minutes == 1 and last != 1:
                        try:
                            await ws_pc.notify_pc(pc.id, json.dumps({"type": "timeleft", "minutes": 1}))
                        except Exception:
                            pass
                        _last_time_warn[pc.id] = 1
                    # Time up: lock once
                    elif minutes <= 0 and last != 0:
                        try:
                            await ws_pc.notify_pc(pc.id, json.dumps({"type": "timeleft", "minutes": 0}))
                            await ws_pc.notify_pc(pc.id, json.dumps({"command": "lock"}))
                        except Exception:
                            pass
                        _last_time_warn[pc.id] = 0
                    # Reset tracker if topped up beyond 5
                    elif minutes > 5 and last in (0, 1, 5):
                        _last_time_warn[pc.id] = None if pc.id in _last_time_warn else None
            finally:
                db.close()
        except Exception:
            pass
        await asyncio.sleep(60)

@app.on_event("startup")
async def _start_background():
    try:
        asyncio.create_task(_broadcast_timeleft_loop())
    except Exception:
        pass
