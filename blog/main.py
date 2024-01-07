from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

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

@app.post('/blog')
def create(request: schema.Blog, db: Session = Depends(getDB)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def all(db: Session = Depends(getDB)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def show(id: int, db: Session = Depends(getDB)):
    blog = db.query(models.Blog).where(models.Blog.id==id).first()
    return blog