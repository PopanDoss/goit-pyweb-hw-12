import os
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv  

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")