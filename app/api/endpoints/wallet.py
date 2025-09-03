from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User, WalletTransaction
from app.schemas import WalletTransactionOut, WalletAction
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

# Get current wallet balance
@router.get("/balance")
def wallet_balance(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=current_user.id).first()
    return {"balance": user.wallet_balance}

# List all wallet transactions for user
@router.get("/transactions", response_model=list[WalletTransactionOut])
def list_transactions(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    txs = db.query(WalletTransaction).filter_by(user_id=current_user.id).order_by(WalletTransaction.timestamp.desc()).all()
    return txs

# Top up wallet (admin or self)
@router.post("/topup", response_model=WalletTransactionOut)
def topup_wallet(
    action: WalletAction, 
    current_user=Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Example: you can add admin check here later
    user = db.query(User).filter_by(id=current_user.id).first()
    user.wallet_balance += action.amount
    tx = WalletTransaction(
        user_id=user.id, amount=action.amount, timestamp=datetime.utcnow(),
        type="topup", description=action.description
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

# Deduct from wallet (used for session billing etc.)
@router.post("/deduct", response_model=WalletTransactionOut)
def deduct_wallet(
    action: WalletAction, 
    current_user=Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(id=current_user.id).first()
    if user.wallet_balance < action.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    user.wallet_balance -= action.amount
    tx = WalletTransaction(
        user_id=user.id, amount=-action.amount, timestamp=datetime.utcnow(),
        type="deduct", description=action.description
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx
