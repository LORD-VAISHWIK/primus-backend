import shutil
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import BackupEntry
from app.schemas import BackupEntryOut
from app.database import SessionLocal
from app.api.endpoints.auth import require_role
from datetime import datetime
import os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Path to your SQLite DB (change if needed)
DB_PATH = "./lance.db"
BACKUP_DIR = "./backups"

os.makedirs(BACKUP_DIR, exist_ok=True)

# Admin: trigger backup
@router.post("/create", response_model=BackupEntryOut)
def create_backup(
    note: str = None,
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    now = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    backup_filename = f"lance_backup_{now}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    try:
        shutil.copyfile(DB_PATH, backup_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backup failed: {str(e)}")
    entry = BackupEntry(
        backup_type="manual",
        file_path=backup_path,
        created_at=datetime.utcnow(),
        note=note
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

# Admin: list all backups
@router.get("/", response_model=list[BackupEntryOut])
def list_backups(
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    return db.query(BackupEntry).order_by(BackupEntry.created_at.desc()).all()

# Admin: download backup (optional, returns file)
from fastapi.responses import FileResponse

@router.get("/download/{backup_id}")
def download_backup(
    backup_id: int,
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    entry = db.query(BackupEntry).filter_by(id=backup_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Backup not found")
    if not os.path.exists(entry.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    return FileResponse(path=entry.file_path, filename=os.path.basename(entry.file_path))

# Admin: restore from backup (overwrites current DB)
@router.post("/restore/{backup_id}")
def restore_backup(
    backup_id: int,
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    entry = db.query(BackupEntry).filter_by(id=backup_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Backup not found")
    try:
        shutil.copyfile(entry.file_path, DB_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Restore failed: {str(e)}")
    return {"message": "Restore completed from backup."}
