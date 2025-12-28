from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
from app.core.security import get_current_user, hash_password

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserRead, UserReadWithPosts
from app.crud import get_user_or_404, is_allow


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user.name, age=user.age, password_hash=hash_password(user.password)
    )
    try:
        db.add(new_user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"User with name {user.name} already exist."
        )

    db.refresh(new_user)

    return new_user


@router.get("/", response_model=list[UserReadWithPosts])
async def get_all_users(
    limit: int = Query(5, ge=1, le=30),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    all_users = (
        db.query(User)
        .options(selectinload(User.posts))
        .offset(offset)
        .limit(limit)
        .all()
    )
    return all_users


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return get_user_or_404(db, user_id)


@router.put("/{user_id}", response_model=UserRead)
async def update_user_by_id(
    user_id: int,
    user_upd: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = get_user_or_404(db, user_id)

    if is_allow(user_id, current_user.id):
        user.name = user_upd.name
        user.age = user_upd.age

        db.commit()
        db.refresh(user)

        return user


@router.delete("/{user_id}", response_model=UserRead)
async def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = get_user_or_404(db, user_id)

    if is_allow(user_id, current_user.id):
        db.delete(user)
        db.commit()
        return user
