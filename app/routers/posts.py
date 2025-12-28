from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.models import Post, User
from app.schemas import PostCreate, PostUpdate, PostRead
from app.crud import get_user_or_404, get_post_or_404, is_allow

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostRead)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    get_user_or_404(db, post.user_id)

    db_post = Post(title=post.title, content=post.content, user_id=post.user_id)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


@router.get("/users/{user_id}/posts", response_model=list[PostRead])
async def get_all_posts_of_user(
    user_id: int,
    limit: int = Query(5, ge=1, le=30),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    get_user_or_404(db, user_id)

    return (
        db.query(Post).filter(Post.user_id == user_id).offset(offset).limit(limit).all()
    )


@router.put("/users/{user_id}/posts/{post_id}", response_model=PostRead)
async def update_post_for_user(
    user_id: int,
    post_id: int,
    updated_post: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = get_post_or_404(db, user_id=user_id, post_id=post_id)

    if is_allow(user_id, current_user.id):
        post.title = updated_post.title
        post.content = updated_post.content
        db.commit()
        db.refresh(post)

        return post


@router.delete("/users/{user_id}/posts/{post_id}", response_model=PostRead)
async def delete_post_for_user(
    user_id: int,
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = get_post_or_404(db, user_id=user_id, post_id=post_id)

    if is_allow(user_id, current_user.id):
        db.delete(post)
        db.commit()

        return post
