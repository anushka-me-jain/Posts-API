from fastapi import APIRouter, Depends, status, HTTPException, APIRouter
from .. database import engine, get_db
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2

router = APIRouter(
    prefix="/vote", 
    tags=["Vote"]
)
@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(vote: schemas.Vote ,db: Session= Depends(get_db),
               current_user: str= Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                             detail = f"post of id {vote.post_id} does not exist") 
    else :
        vote_query = db.query(models.Vote).filter(models.Vote.user_id== vote.user_id,
                                                    models.Vote.post_id == vote.post_id)
        found_vote = vote_query.first()  
        if vote.dir==1:
            if found_vote:
                raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                                        detail= f"vote with id {vote.post_id} already exits")
            new_vote = models.Vote(user_id = vote.user_id, post_id = vote.post_id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return {"message": "vote added"}        
        else :
            if not found_vote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            db.delete(found_vote)
            db.commit()
            return {"message": "deleted"}