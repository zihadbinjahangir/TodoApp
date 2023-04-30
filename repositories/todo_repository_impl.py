from sqlalchemy.orm import Session
from typing import List
from models.todo import Todos
from schemas.todos import TodoSchema
from repositories.todo_repository import TodoRepository

class TodoRepositoryImpl(TodoRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def create_todo(self, todo: TodoSchema, user_id) -> Todos:
        todo_model = Todos()
        todo_model.title = todo.title
        todo_model.description = todo.description
        todo_model.priority = todo.priority
        todo_model.complete = todo.complete
        todo_model.owner_id = user_id

        self.db.add(todo_model)
        self.db.commit()

        return todo_model
    
    def get_all_todo(self) -> List[Todos]:
        return self.db.query(Todos).all()
    
    def get_all_todos_by_user(self, user_id) -> List[Todos]:
        return self.db.query(Todos).filter(Todos.owner_id == user_id).all()
    
    def get_todo_by_id(self, owner_id, todo_id) -> Todos:
        return self.db.query(Todos)\
            .filter(Todos.owner_id == owner_id)\
            .filter(Todos.id == todo_id).first()
    
    def update_a_todo(self, todo: TodoSchema, owner_id, todo_id) -> Todos:

        todo_model = self.db.query(Todos)\
        .filter(Todos.owner_id == owner_id)\
        .filter(Todos.id == todo_id).first()

        if todo_model is not None:
            todo_model.title = todo.title
            todo_model.description = todo.description
            todo_model.priority = todo.priority
            todo_model.complete = todo.complete

            self.db.add(todo_model)
            self.db.commit()
            return todo_model
        
    def delet_a_todo(self, owner_id, todo_id) -> Todos:

        todo_model = self.db.query(Todos)\
        .filter(Todos.owner_id == owner_id)\
        .filter(Todos.id == todo_id).first()

        if todo_model is not None:
            self.db.query(Todos)\
            .filter(Todos.owner_id == owner_id)\
            .filter(Todos.id == todo_id).delete()
            self.db.commit()
            return todo_model