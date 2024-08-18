from .. import models, schemas, oauth2
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from typing import List
from ..database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

router = APIRouter(prefix="/posts", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    # cursor.execute('''INSERT INTO posts(title, content, published) VALUES (%s, %s, %s)
    #                   RETURNING*''',(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=list[schemas.PostResponse])
def get_posts(
    db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)
):
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("count1"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .order_by(models.Post.created_at.desc())
        .all()
    )
    # posts = db.query(models.Post).all()

    return posts
    # return [schemas.PostResponse.from_orm(post) for post, count1 in posts]


# @router.get("/{id}" )
@router.get("/{id}", response_model=schemas.SinglePostResponse)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    votes = db.query(models.Vote).filter(models.Vote.post_id == id).count()
    self_vote = (
        db.query(models.Vote)
        .filter(models.Vote.post_id == id, models.Vote.user_id == current_user.id)
        .count()
    )

    return {"Post": post, "count1": votes, "self_voted": self_vote}


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING*""",

    #             (post.title, post.content, post.published, str(id,)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not authorized to perform requested action ",
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


# get method url : "/ "


@router.delete("/{id}")
def delete_posts(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    # cursor.execute("DELETE FROM posts WHERE id = %s returning* ", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist",
        )

    if post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_200_OK)
