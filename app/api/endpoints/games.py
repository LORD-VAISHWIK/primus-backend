from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Game, User
from app.schemas import GameCreate, GameUpdate, Game
from app.api.endpoints.auth import get_current_user
from app.api.endpoints.audit import log_action

router = APIRouter()

@router.get("", response_model=List[Game])
def list_games(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    category: Optional[str] = None,
    enabled: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """List games with optional filtering and pagination"""
    query = db.query(Game)
    
    if search:
        query = query.filter(Game.name.ilike(f"%{search}%"))
    
    if category:
        query = query.filter(Game.category == category)
    
    if enabled is not None:
        query = query.filter(Game.enabled == enabled)
    
    games = query.offset(skip).limit(limit).all()
    return games

@router.get("/count")
def get_games_count(
    search: Optional[str] = None,
    category: Optional[str] = None,
    enabled: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """Get total count of games with optional filtering"""
    query = db.query(Game)
    
    if search:
        query = query.filter(Game.name.ilike(f"%{search}%"))
    
    if category:
        query = query.filter(Game.category == category)
    
    if enabled is not None:
        query = query.filter(Game.enabled == enabled)
    
    count = query.count()
    return {"count": count}

@router.post("", response_model=Game)
def create_game(
    game: GameCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new game"""
    # Check if game with same name already exists
    existing = db.query(Game).filter(Game.name == game.name).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Game with name '{game.name}' already exists"
        )
    
    db_game = Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    
    # Log the action
    log_action(
        db, current_user.id,
        "game_created",
        f"Created game: {game.name}"
    )
    
    return db_game

@router.put("/{game_id}", response_model=Game)
def update_game(
    game_id: int,
    game_update: GameUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing game"""
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Update only provided fields
    update_data = game_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_game, field, value)
    
    db_game.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(db_game)
    
    # Log the action
    log_action(
        db, current_user.id,
        "game_updated",
        f"Updated game: {db_game.name}"
    )
    
    return db_game

@router.delete("/{game_id}")
def delete_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a game"""
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game_name = db_game.name
    db.delete(db_game)
    db.commit()
    
    # Log the action
    log_action(
        db, current_user.id,
        "game_deleted",
        f"Deleted game: {game_name}"
    )
    
    return {"message": f"Game '{game_name}' deleted successfully"}

@router.post("/bulk-toggle")
def bulk_toggle_games(
    game_ids: List[int],
    enabled: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Bulk toggle games enabled/disabled status"""
    games = db.query(Game).filter(Game.id.in_(game_ids)).all()
    
    for game in games:
        game.enabled = enabled
        game.last_updated = datetime.utcnow()
    
    db.commit()
    
    # Log the action
    log_action(
        db, current_user.id,
        "games_bulk_toggled",
        f"Bulk {'enabled' if enabled else 'disabled'} {len(games)} games"
    )
    
    return {"message": f"{len(games)} games {'enabled' if enabled else 'disabled'} successfully"}
