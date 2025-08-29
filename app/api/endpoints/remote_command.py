from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import RemoteCommand, PC
from app.schemas import RemoteCommandIn, RemoteCommandOut
from app.ws.pc import notify_pc
import json
from app.database import SessionLocal
from app.api.endpoints.auth import get_current_user
from app.api.endpoints.audit import log_action
from datetime import datetime
from app.api.endpoints.auth import require_role

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Admin sends a command to a PC
@router.post("/send", response_model=RemoteCommandOut)
async def send_command(
    cmd: RemoteCommandIn,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # (Optional: check admin permissions here)
    pc = db.query(PC).filter_by(id=cmd.pc_id).first()
    if not pc:
        raise HTTPException(status_code=404, detail="PC not found")
    rc = RemoteCommand(
        pc_id=cmd.pc_id,
        command=cmd.command,
        params=cmd.params,
        issued_at=datetime.utcnow(),
        executed=False
    )
    db.add(rc)
    db.commit()
    db.refresh(rc)
    try:
        log_action(db, getattr(current_user,'id',None), f'pc_command:{cmd.command}', f'PC:{cmd.pc_id} params:{cmd.params}', None)
    except Exception:
        pass
    # Push to PC websocket (best-effort)
    try:
        payload = json.dumps({
            "pc_id": cmd.pc_id,
            "command": cmd.command,
            "params": cmd.params
        })
        await notify_pc(cmd.pc_id, payload)
    except Exception:
        pass
    return rc

# Client fetches the latest command (and marks it executed)
@router.post("/fetch", response_model=RemoteCommandOut | None)
def fetch_command(
    pc_id: int,
    db: Session = Depends(get_db)
):
    rc = db.query(RemoteCommand).filter_by(pc_id=pc_id, executed=False).order_by(RemoteCommand.issued_at.desc()).first()
    if rc:
        rc.executed = True
        db.commit()
        db.refresh(rc)
        return rc
    return None

# Admin can see history (optional)
@router.get("/history/{pc_id}", response_model=list[RemoteCommandOut])
def command_history(
    pc_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cmds = db.query(RemoteCommand).filter_by(pc_id=pc_id).order_by(RemoteCommand.issued_at.desc()).all()
    return cmds

