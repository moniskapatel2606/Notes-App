from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)

    user_id=Column(Integer,ForeignKey('users.id'))

    creator=relationship('User', back_populates='note')


class User(Base):
    __tablename__ = 'users'

    id= Column(Integer, primary_key=True, index=True)
    username = Column(String,unique=True)
    email = Column(String,unique=True)
    password= Column(String)
 
    note=relationship('Note', back_populates='creator')



