from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import ChatMessage
from app.schemas import ChatMessageIn, ChatMessageOut
from app.database import SessionLocal
from app.api.endpoints.auth import get_current_user
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Send message
@router.post("/", response_model=ChatMessageOut)
def send_message(
    msg: ChatMessageIn,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cm = ChatMessage(
        from_user_id=current_user.id,
        to_user_id=msg.to_user_id,
        pc_id=msg.pc_id,
        message=msg.message,
        timestamp=datetime.utcnow(),
        read=False
    )
    db.add(cm)
    db.commit()
    db.refresh(cm)
    return cm

# Get my messages (latest first)
@router.get("/", response_model=list[ChatMessageOut])
def my_messages(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    msgs = db.query(ChatMessage).filter(
        (ChatMessage.to_user_id == current_user.id) | (ChatMessage.to_user_id == None)
    ).order_by(ChatMessage.timestamp.desc()).all()
    return msgs
