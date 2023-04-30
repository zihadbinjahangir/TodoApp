from abc import ABC, abstractmethod
from models.user import Users

class UserRepository(ABC):

    @abstractmethod
    def create_user(self, user: Users) -> Users:
        pass

    @abstractmethod
    def get_user(user_name:str) -> Users:
        pass