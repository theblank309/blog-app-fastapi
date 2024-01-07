from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
import uvicorn

from blog import schema, models
from blog.database import engine, SessionLocal

models.Base.metadata.create_all(engine)

app = FastAPI()

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schema.Blog, db: Session = Depends(getDB)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(getDB)):
    db.query(models.Blog).where(models.Blog.id == id).delete()
    db.commit()
    return "deleted"

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schema.Blog, db: Session = Depends(getDB)):
    db.query(models.Blog).where(models.Blog.id == id).update({'title': request.title, 'body': request.body})
    db.commit()
    return "updated"

@app.get('/blog', status_code=status.HTTP_200_OK)
def all(db: Session = Depends(getDB)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def show(id: int, db: Session = Depends(getDB)):
    blog = db.query(models.Blog).where(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"blog with id {id} not found")
    return blog

if __name__ == "__main__":
    uvicorn.run("blog.main:app", host="127.0.0.1", port=8000, reload=True)