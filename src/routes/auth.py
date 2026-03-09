from typing import Any

from fastapi import APIRouter, HTTPException, Depends, status, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.dependency_injection.di import get_db_session
from src.schemas.schemas import UserModel, UserResponse, TokenModel, UserDB
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.database.models import User

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(body: UserModel, db: Session = Depends(get_db_session)) -> dict[str, Any]:
    exist_user = repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = repository_users.create_user(body, db)
    return {"user": new_user, "detail": "User successfully created"}


@router.post("/login", response_model=TokenModel)
def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)) -> dict[str, str]:
    print(f"DEBUG: Received password: '{body.password}'")
    user = repository_users.get_user_by_email(body.username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # if not auth_service.verify_password(body.password, user.password):
    is_valid = auth_service.verify_password(body.password, user.password)
    print(f"DEBUG: Password verification: {is_valid}")
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Generate JWT
    access_token = auth_service.create_access_token(data={"sub": user.email})
    refresh_token = auth_service.create_refresh_token(data={"sub": user.email})
    repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db_session)) -> dict[str, str]:
    token = credentials.credentials
    email = auth_service.decode_refresh_token(token)
    user = repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = auth_service.create_access_token(data={"sub": email})
    refresh_token = auth_service.create_refresh_token(data={"sub": email})
    repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get('/me', response_model=UserDB)
def me(current_user: User = Depends(auth_service.get_current_user)) -> User:
    return current_user