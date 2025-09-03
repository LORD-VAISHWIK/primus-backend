from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.models import AuditLog
from app.schemas import AuditLogOut
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

# Utility: log an action (call from other endpoints!)
def log_action(db, user_id, action, detail, ip=None):
    entry = AuditLog(
        user_id=user_id,
        action=action,
        detail=detail,
        ip=ip,
        timestamp=datetime.utcnow()
    )
    db.add(entry)
    db.commit()

# List logs (admin only)
@router.get("/", response_model=list[AuditLogOut])
def list_logs(
    start: str | None = None,
    end: str | None = None,
    category: str | None = None,
    pc: str | None = None,
    employee: str | None = None,
    user: str | None = None,
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    q = db.query(AuditLog)
    from datetime import datetime as _dt
    if start:
        try: q = q.filter(AuditLog.timestamp >= _dt.fromisoformat(start))
        except: pass
    if end:
        try: q = q.filter(AuditLog.timestamp <= _dt.fromisoformat(end))
        except: pass
    if category:
        q = q.filter(AuditLog.action.ilike(f"%{category}%"))
    if user:
        # naive: search in detail or require user_id match if numeric
        try:
            uid = int(user)
            q = q.filter(AuditLog.user_id == uid)
        except:
            q = q.filter(AuditLog.detail.ilike(f"%{user}%"))
    # pc/employee filters can be encoded in detail for now
    if pc:
        q = q.filter(AuditLog.detail.ilike(f"%PC:{pc}%"))
    if employee:
        q = q.filter(AuditLog.detail.ilike(f"%Employee:{employee}%"))
    logs = q.order_by(AuditLog.timestamp.desc()).limit(1000).all()
    return logs

# (Optional) Get user-specific logs
@router.get("/user/{user_id}", response_model=list[AuditLogOut])
def user_logs(
    user_id: int,
    current_user=Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    logs = db.query(AuditLog).filter_by(user_id=user_id).order_by(AuditLog.timestamp.desc()).limit(100).all()
    return logs

# Client-originated audit log (auth optional; prefer with JWT)
@router.post("/client")
def client_log(payload: dict, request: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        action = payload.get("action")
        detail = payload.get("detail")
        if not action:
            raise HTTPException(status_code=400, detail="action required")
        uid = getattr(current_user, 'id', None)
        log_action(db, uid, action, detail or "", ip=str(request.client.host))
        return {"status": "ok"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="invalid payload")
