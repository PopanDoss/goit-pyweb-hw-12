from typing import Optional
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database.models import User

from repository.auth import create_access_token, create_refresh_token, Hash, get_email_form_refresh_token
from shemas import UserModel

hash_handler = Hash()

class UsernameTaken(Exception):
    pass

class LoginFailed(Exception):
    pass 

class InvalidRefreshtoken(Exception):
    pass



class UserService: 

    @staticmethod
    def get_user(username: str, db: Session) -> Optional[User]:
        return db.query(User).filter(User.email == username).first()



    @staticmethod
    def check_username_availablity(username: str, db: Session):
        exist_user = UserService.get_user(username, db)
        if exist_user:
            raise UsernameTaken
        

    @staticmethod
    def check_password(entered_password: str, database_password: str ):
        if not hash_handler.verify_password(body.password, user.password):
            raise UserWrongPassword
        return exist_user

        
    @staticmethod
    def creat_new_user(body: UserModel, db: Session ):
        UserService.check_username_availablity(username=body.username, db=db )
        new_user = User(email=body.username, password=hash_handler.get_password_hash(body.password))
        new_user = UserService.save_user(new_user, db)
        return new_user
    
    @staticmethod
    def login_user(body: OAuth2PasswordRequestForm, db: Session):
        user = UserService.get_user(body.username, db = db )
        if user is None or not hash_handler.verify_password(body.password, user.password):
            raise  LoginFailed
        
        data={"sub": user.email}
        access_token = create_access_token(data=data)
        refresh_token = create_refresh_token(data=data)
        user.refresh_token = refresh_token
        
        UserService.save_user(user, db)
        return access_token, refresh_token
    
    @staticmethod
    def refresh_token(refresh_token: str, db: Session):
        email = get_email_form_refresh_token(refresh_token)
        user = UserService.get_user(email, db)
        if user.refresh_token != refresh_token:
            user.refresh_token = None
            UserService.save_user(user, db)
            raise InvalidRefreshtoken

        access_token = create_access_token(data={"sub": email})
        return access_token
    
    @staticmethod
    def save_user(user_to_save, db: Session) -> User:
        db.add(user_to_save)
        db.commit()
        db.refresh(user_to_save)
        return user_to_save