from libgravatar import Gravatar  # type: ignore -> ignore mypy error for this import
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas.schemas import UserModel


""" class Gravatar:
    def __init__(self, email: str) -> None: ...
    def get_image(self, *args, **kwargs) -> str: ...
    def get_image_url(self, *args, **kwargs) -> str: ... """


def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()
