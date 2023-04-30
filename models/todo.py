from sqlalchemy import Integer, Boolean, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="todos")