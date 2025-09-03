from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Webhook
from app.schemas import WebhookIn, WebhookOut
from app.database import SessionLocal
from app.api.endpoints.auth import require_role, get_current_user
from datetime import datetime
import requests # pyright: ignore[reportMissingModuleSource]

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Admin: create webhook
@router.post("/", response_model=WebhookOut)
def create_webhook(
    wh: WebhookIn,
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    webhook = Webhook(
        url=wh.url,
        event=wh.event,
        secret=wh.secret,
        created_at=datetime.utcnow(),
        is_active=True
    )
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook

# List all webhooks
@router.get("/", response_model=list[WebhookOut])
def list_webhooks(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Webhook).all()

# Deactivate webhook
@router.post("/deactivate/{webhook_id}")
def deactivate_webhook(
    webhook_id: int,
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    wh = db.query(Webhook).filter_by(id=webhook_id).first()
    if not wh:
        raise HTTPException(status_code=404, detail="Webhook not found")
    wh.is_active = False
    db.commit()
    return {"message": "Webhook deactivated"}
