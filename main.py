import uuid

from fastapi import FastAPI, status
from sqlalchemy import Column, Integer, String, CHAR
from sqlalchemy.ext.declarative import declarative_base



#engine = create_engine("sqlite://user.db")
#Base = declarative_base()
#Base.metadata.create_all(engine)
app = FastAPI()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    gender = Column(CHAR, unique=True, index=True)
    password_hash = Column(String)


@app.get("/")
def root():
    return "root"
@app.post("/user", status_code=201)
def create_user():
    return "create user item"

@app.get("/user/{id}")
def read_user(id: int):
    return "read user item with id {id}"
@app.put("/user/{id}")
def update_user(id: int):
    return "update user item"
@app.delete("/user/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: int):
    return "delete user item"
@app.get("/user")
def read_user_list():
    return "read user list"

