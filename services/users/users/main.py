from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Session, create_engine
from datetime import timedelta
from users.models import User
from users.schemas import UserCreate, UserResponse, UserLogin, UserProfile
from users.crud import create_user, authenticate_user, get_user_by_username
from users.security import create_access_token, verify_token
from users.security import ACCESS_TOKEN_EXPIRE_MINUTES

DATABASE_URL = "postgresql://user:password@db/user_db"
engine = create_engine(DATABASE_URL)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/register/", response_model=UserResponse)
def register_user(user: UserCreate):
    with Session(engine) as session:
        db_user = get_user_by_username(session, user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        return create_user(session, user)

@app.post("/token", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        user = authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=UserProfile)
def read_users_me(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_token(token, credentials_exception)
    with Session(engine) as session:
        user = get_user_by_username(session, username)
        if user is None:
            raise credentials_exception
        return user
