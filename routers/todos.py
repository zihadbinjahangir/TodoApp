from fastapi import APIRouter, Depends, HTTPException
from models import todo
from database import engine, Sessionlocal
from sqlalchemy.orm import Session
from .auth import get_current_user, user_not_found_exception
from schemas.todos import TodoSchema
from repositories.todo_repository_impl import TodoRepositoryImpl

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404:{"description":"Not found"}}
)

todo.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = Sessionlocal()
        yield db
    finally:
        db.close()

@router.get("/")
async def read_all_todos(db : Session = Depends(get_db)):
    todo_repo = TodoRepositoryImpl(db)
    return todo_repo.get_all_todo()

@router.get("/user")
async def read_all_todos_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise user_not_found_exception()
    todo_repo = TodoRepositoryImpl(db)
    return todo_repo.get_all_todos_by_user(user["user_id"])

@router.get("/{todo_id}")
async def read_todo(todo_id : int, user: dict = Depends(get_current_user), db : Session = Depends(get_db)):
    
    if user is None:
        raise user_not_found_exception()
    
    todo_repo = TodoRepositoryImpl(db)
    todo_model = todo_repo.get_todo_by_id(user["user_id"], todo_id)

    if todo_model is not None:
        return todo_model
    raise http_exception()

@router.post('/')
async def creat_todo(todo: TodoSchema, user: dict = Depends(get_current_user), db : Session = Depends(get_db)):
    
    if user is None:
        raise user_not_found_exception()
    
    todo_repo = TodoRepositoryImpl(db)
    todo_model = todo_repo.create_todo(todo, user["user_id"])

    return {
        "status":201,
        "transaction":"Successful"
    }

@router.put("/{todo_id}")
async def update_todo(todo_id:int, todo: TodoSchema, user: dict = Depends(get_current_user), db:Session = Depends(get_db)):
    
    if user is None:
        raise user_not_found_exception()
    
    todo_repo = TodoRepositoryImpl(db)
    todo_model = todo_repo.update_a_todo(todo, user["user_id"], todo_id)

    if todo_model is None:
        raise http_exception

    return {
        "status":200,
        "transaction":"Successful"
    }

@router.delete("/{todo_id}")
async def delete_todo(todo_id:int, user: dict = Depends(get_current_user), db:Session = Depends(get_db)):
    
    if user is None:
        raise user_not_found_exception()
    
    todo_repo = TodoRepositoryImpl(db)
    todo_model = todo_repo.delet_a_todo(user["user_id"], todo_id)

    if todo_model is None:
        raise http_exception

    return {
        "status":200,
        "transaction":"Successful"
    }

def http_exception():
    return HTTPException(status_code=404, detail="Item not found")