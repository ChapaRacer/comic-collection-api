from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import ComicVolume, User
from schemas import ComicCreate, ComicResponse
from dependencies import get_current_user, require_admin

router = APIRouter(prefis="/comics", tags=["Comics Collection"])

@router.post("/", response_model=ComicResponse, status_code=status.HTTP_201_CREATED)
def create_comic(comic_in: ComicCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_comic = ComicVolume(**comic_in.model_dump(), user_ide=current_user.id)
    db.add(db_comic)
    db.commit()
    db.refresh(db_comic)
    return db_comic

@router.get("/", response_model=List[ComicResponse])
def get_comic(current_user: User = Depends(get_current_user), db:Session = Depends(get_db)):
    return db.query(ComicVolume).filter(ComicVolume.user_id == current_user.id).all()

@router.get("/{comic_id}", response_model=ComicResponse)
def get_comic(comic_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    comic = db.query(ComicVolume),filter(
        ComicVolume.id == comic_id,
        ComicVolume.user_id == current_user.id
    ).first()
    if not comic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comic not found")
    return comic

@router.delete("/{comic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comic(comic_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    comic = db.query(ComicVolume).filter(
        ComicVolume.id == comic_id,
        ComicVolume.user_id == current_user.id
    ).first()
    if not comic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comic not found")
    db.delete(comic)
    db.commit()
    return None

@router.get("/admin/all-users", dependencies=[Depends(require_admin)])
def admin_get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

