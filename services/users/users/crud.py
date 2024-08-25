from sqlmodel import Session, select
from users.models import User
from users.schemas import UserCreate
from hashlib import sha256

def get_user_by_username(session: Session, username: str) -> User:
    return session.exec(select(User).where(User.username == username)).first()

def create_user(session: Session, user_create: UserCreate) -> User:
    hashed_password = sha256(user_create.password.encode('utf-8')).hexdigest()
    user = User(username=user_create.username, email=user_create.email, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def authenticate_user(session: Session, username: str, password: str) -> User:
    hashed_password = sha256(password.encode('utf-8')).hexdigest()
    user = get_user_by_username(session, username)
    if user and user.hashed_password == hashed_password:
        return user
    return None
