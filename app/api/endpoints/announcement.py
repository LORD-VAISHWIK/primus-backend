from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Announcement
from app.schemas import AnnouncementIn, AnnouncementOut
from app.database import SessionLocal
from app.api.endpoints.auth import get_current_user, require_role
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Admin: create announcement
@router.post("/", response_model=AnnouncementOut)
def create_announcement(
    ann: AnnouncementIn,
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    a = Announcement(
        content=ann.content,
        type=ann.type,
        created_at=datetime.utcnow(),
        start_time=ann.start_time,
        end_time=ann.end_time,
        target_role=ann.target_role,
        active=True
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

# List all current announcements (for client display)
@router.get("/", response_model=list[AnnouncementOut])
def list_announcements(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    now = datetime.utcnow()
    query = db.query(Announcement).filter(Announcement.active == True)
    query = query.filter(
        (Announcement.start_time == None) | (Announcement.start_time <= now)
    ).filter(
        (Announcement.end_time == None) | (Announcement.end_time >= now)
    )
    # Filter by role if set
    if current_user.role and current_user.role != "admin":
        query = query.filter(
            (Announcement.target_role == None) | (Announcement.target_role == current_user.role)
        )
    return query.order_by(Announcement.created_at.desc()).all()

# Admin: deactivate (hide) an announcement
@router.post("/deactivate/{ann_id}")
def deactivate_announcement(
    ann_id: int,
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    a = db.query(Announcement).filter_by(id=ann_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Announcement not found")
    a.active = False
    db.commit()
    return {"message": "Announcement deactivated."}
