from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.models import Post, Tag, User
from app.schemas import PostCreate, PostUpdate, PostRead, TagsAdd
from app.crud import get_user_or_404, get_post_or_404, is_allow

router = APIRouter(prefix="/posts", tags=["tags"])


@router.post("/{post_id}/tags")
def add_tags_to_post(post_id: int, tags: TagsAdd, db: Session = Depends(get_db)):
    post = get_post_or_404(db, post_id=post_id)

    for one_tag in tags.words:
        tag = db.query(Tag).filter(Tag.word == one_tag.word).first()

        if not tag:
            tag = Tag(word=one_tag.word)
            db.add(tag)

        if tag not in post.tags:
            post.tags.append(tag)

    db.commit()
    db.refresh(post)
    return post.tags
