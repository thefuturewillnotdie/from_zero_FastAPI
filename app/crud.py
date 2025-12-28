from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from app.core.security import get_current_user
from app.models import User, Post


def get_user_or_404(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with {user_id} ID not found."
        )
    return user


def get_post_or_404(db: Session, *, user_id: int | None = None, post_id: int):
    query = db.query(Post).filter(Post.id == post_id)

    if user_id is not None:
        query = query.filter(Post.user_id == user_id)

    post = query.first()

    if not post:
        if user_id is not None:
            raise HTTPException(
                status_code=404, detail=f"User {user_id} has no post with ID {post_id}."
            )
        raise HTTPException(
            status_code=404, detail=f"Post with ID {post_id} not found."
        )
    return post


def is_allow(user_id: int, current_user: int):
    if user_id != current_user:
        raise HTTPException(
            status_code=403, detail="You are not allowed to update this post."
        )
    else:
        return True
