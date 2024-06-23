from fastapi import APIRouter, HTTPException, Depends, status, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.orm import Session

from typing import List

from datetime import date

from shemas import UserModel
from database.db import get_db

from repository.users_crud import UserService, UsernameTaken, LoginFailed


router = APIRouter(prefix= '/users', tags=['users'])

security = HTTPBearer()
user_servis = UserService()

@router.post("/signup")
async def signup(body: UserModel, db: Session = Depends(get_db)):
    try:  
        new_user = user_servis.creat_new_user(body, db)  
    except UsernameTaken:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    
    return {"new_user": new_user.email} 


@router.post("/login")
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        access_token, refresh_token = user_servis.login_user(body, db)
    except LoginFailed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": access_token, "refresh_token": refresh_token,  "token_type": "bearer"}


@router.post('/refresh_token')
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    access_token = user_servis.refresh_token(token, db)
    
    return {"access_token": access_token, "refresh_token": token, "token_type": "bearer"}