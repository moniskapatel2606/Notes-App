from fastapi import FastAPI,Depends , HTTPException
from . import schemas,models,hashing,token,oauth2
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordRequestForm



models.Base.metadata.create_all(bind=engine)

app=FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def index():
    return 'Hello wolrd'

@app.post('/notes',status_code=201 , tags=['Notes'])
def create_notes( request:schemas.Note ,user:str=Depends(token.get_current_user_id), db:Session=Depends(get_db),current_user:schemas.User=Depends( oauth2.get_current_user)):
    new_note= models.Note(title=request.title,content=request.content,user_id=user)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.get('/notes',response_model=List[schemas.ShowNote],tags=['Notes'])
def all_notes( db:Session=Depends(get_db),current_user:schemas.User=Depends( oauth2.get_current_user)):

    return db.query(models.Note).all()

@app.get('/notes/{id}',status_code=200,response_model=schemas.ShowNote,tags=['Notes'])
def single_note( id:int, db:Session=Depends(get_db),current_user:schemas.User=Depends( oauth2.get_current_user)):
    if note := db.query(models.Note).filter(models.Note.id == id).first():
        return note
    else:
         raise HTTPException(status_code=404,detail='Note not found')


@app.post('/register',response_model=schemas.ShowUser,tags=['User'])
def craete_user(request:schemas.User,db:Session=Depends(get_db)):
    new_user=models.User(username=request.username,email=request.email,password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# @app.post('/user/{id}',response_model=schemas.ShowUser,tags=['User'])
# def get_user(id:int,db:Session=Depends(get_db)):
#     user=db.query(models.User).filter(models.User.id==id).first()
#     if not user:
#         raise HTTPException(status_code=404,detail='user not found')
#     return user


@app.post("/login",tags=['login'])
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email ==request.username).first()
    if not user:
        raise HTTPException(status_code=404,detail='Incorrect Username')
    if not hashing.Hash.verify( user.password,request.password):
        raise HTTPException(status_code=404,detail='Incorrect Password')
    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
