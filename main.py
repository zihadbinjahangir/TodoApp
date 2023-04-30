from fastapi import FastAPI
from models import user,todo
from database import engine
from routers import auth,todos

app = FastAPI()
user.Base.metadata.create_all(bind=engine)
todo.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)