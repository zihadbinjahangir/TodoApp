from abc import ABC, abstractmethod
from typing import List
from models.todo import Todos
from schemas.todos import TodoSchema

class TodoRepository(ABC):

    @abstractmethod
    def create_todo(self, todo: TodoSchema, user_id) -> Todos:
        pass

    @abstractmethod
    def get_all_todo(self) -> List[Todos]:
        pass

    @abstractmethod
    def get_all_todos_by_user(self, user_id) -> List[Todos]:
        pass

    @abstractmethod
    def get_todo_by_id(self, owner_id, todo_id) -> Todos:
        pass

    @abstractmethod
    def update_a_todo(self, todo:TodoSchema, owner_id, todo_id) -> Todos:
        pass

    @abstractmethod
    def delet_a_todo(self, owner_id, todo_id) -> Todos:
        pass
