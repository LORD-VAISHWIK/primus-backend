from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.models import Screenshot, PC
from app.database import SessionLocal
from app.api.endpoints.auth import get_current_user, require_role
from datetime import datetime
import os

router = APIRouter()
UPLOAD_DIR = "./screenshots"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# PC posts a screenshot
@router.post("/upload/{pc_id}")
async def upload_screenshot(
    pc_id: int,
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    filename = f"{pc_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.png"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    ss = Screenshot(
        pc_id=pc_id,
        image_url=filepath,
        timestamp=datetime.utcnow(),
        taken_by=current_user.id
    )
    db.add(ss)
    db.commit()
    db.refresh(ss)
    return {"image_url": filepath}

# Admin: List latest screenshots per PC
@router.get("/latest", tags=["screenshot"])
def latest_screenshots(current_user=Depends(require_role("admin")), db: Session = Depends(get_db)):
    pcs = db.query(PC).all()
    results = []
    for pc in pcs:
        ss = db.query(Screenshot).filter_by(pc_id=pc.id).order_by(Screenshot.timestamp.desc()).first()
        if ss:
            results.append({
                "pc_id": pc.id,
                "image_url": ss.image_url,
                "timestamp": ss.timestamp
            })
    return results
