from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse, PlainTextResponse
from app.database import SessionLocal
from app.models import User
from app.api.endpoints.auth import get_current_user, require_role
from app.api.endpoints.auth import RegisterIn  # reuse schema
from datetime import datetime
import io
import csv
from passlib.hash import bcrypt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[dict])
def list_users(current_user=Depends(require_role("admin")), db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id.asc()).all()
    out = []
    for u in users:
        out.append({
            "id": u.id,
            "username": u.name,
            "email": u.email,
            "role": u.role,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "phone": u.phone,
            "coins_balance": 0,
            "account_balance": 0,
            "user_group": None,
            "start_date": None,
            "end_date": None,
        })
    return out

@router.post("/create")
def create_user(payload: RegisterIn, current_user=Depends(require_role("admin")), db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = bcrypt.hash(payload.password)
    bd = None
    if payload.birthdate:
        try:
            bd = datetime.strptime(payload.birthdate, "%d/%m/%Y")
        except Exception:
            try:
                bd = datetime.fromisoformat(payload.birthdate)
            except Exception:
                bd = None
    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hashed,
        role=payload.role or "client",
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone=payload.phone,
        birthdate=bd,
        is_email_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"ok": True, "id": user.id}

@router.get("/export")
def export_users(current_user=Depends(require_role("admin")), db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id.asc()).all()
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["username", "email", "role", "first_name", "last_name", "phone"])
    for u in users:
        writer.writerow([u.name or "", u.email or "", u.role or "client", u.first_name or "", u.last_name or "", u.phone or ""])
    buf.seek(0)
    return StreamingResponse(iter([buf.read()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=users.csv"})

@router.post("/import")
def import_users(file: UploadFile = File(...), current_user=Depends(require_role("admin")), db: Session = Depends(get_db)):
    # Expect CSV with headers: username,email,password,first_name,last_name,phone,role
    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    created = 0
    errors: list[str] = []
    for i, row in enumerate(reader, start=2):
        try:
            name = (row.get("username") or row.get("name") or "").strip()
            email = (row.get("email") or "").strip()
            password = (row.get("password") or "").strip()
            if not email or not password or not name:
                errors.append(f"row {i}: missing username/email/password")
                continue
            if db.query(User).filter(User.email == email).first():
                continue
            user = User(
                name=name,
                email=email,
                password_hash=bcrypt.hash(password),
                role=(row.get("role") or "client").strip() or "client",
                first_name=(row.get("first_name") or "").strip() or None,
                last_name=(row.get("last_name") or "").strip() or None,
                phone=(row.get("phone") or "").strip() or None,
                is_email_verified=True,
            )
            db.add(user)
            created += 1
        except Exception as e:
            errors.append(f"row {i}: {e}")
    db.commit()
    return {"created": created, "errors": errors}


