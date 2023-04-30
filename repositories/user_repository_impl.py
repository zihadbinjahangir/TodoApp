from sqlalchemy.orm import Session
from models.user import Users
from schemas.user import UserSchema
from repositories.user_repository import UserRepository

class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user: UserSchema, bcrypt_password) -> Users:
        creat_user_model = Users()

        creat_user_model.email = user.email
        creat_user_model.username = user.username
        creat_user_model.first_name = user.first_name
        creat_user_model.last_name = user.last_name
        creat_user_model.hashed_password = bcrypt_password
        creat_user_model.is_active = user.is_active

        self.db.add(creat_user_model)
        self.db.commit()
        return creat_user_model
    
    def get_user(self,user_name:str) -> Users:
        user = self.db.query(Users).filter(Users.username == user_name).first()
        return user
