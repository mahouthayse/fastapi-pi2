from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

origins = [
    "http://localhost:5173",
    "http://localhost:8080",
]
engine = create_engine('postgresql://postgres:root@localhost/PI2CRUD')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(128))
    age = Column(Integer)
    cpf = Column(String(64), unique=True)
    gender = Column(String(16))
    email = Column(String(64), unique=True, nullable=False)
    zipcode = Column(String(64))
    address = Column(String(128))
    address_number = Column(String(16))
    address_neighborhood = Column(String(64))
    address_city = Column(String(64))
    address_state = Column(String(64))
    password = Column(String(128), nullable=False)

Base.metadata.create_all(bind=engine)

class UserCreateUpdateModel(BaseModel):
    name: str
    age: int
    cpf: str
    gender: str
    email: str
    zipcode: str
    address: str
    address_number: str
    address_neighborhood: str
    address_city: str
    address_state: str
    password: str


@app.get("/")
def root():
    return "root"

@app.post("/users")
def create_user(user_data: UserCreateUpdateModel):
    db = SessionLocal()
    db_user = User(
        name=user_data.name,
        age=user_data.age,
        cpf=user_data.cpf,
        gender=user_data.gender,
        email=user_data.email,
        zipcode=user_data.zipcode,
        address=user_data.address,
        address_number=user_data.address_number,
        address_neighborhood=user_data.address_neighborhood,
        address_city=user_data.address_city,
        address_state=user_data.address_state,
        password=user_data.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return JSONResponse(content={"message": "Usuário criado com sucesso"})

@app.get("/users/{id}")
def get_user(id: str):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    user_dict = {
        "id": str(user.id),
        "name": user.name,
        "age": user.age,
        "cpf": user.cpf,
        "gender": user.gender,
        "email": user.email,
        "zipcode": user.zipcode,
        "address": user.address,
        "address_number": user.address_number,
        "address_neighborhood": user.address_neighborhood,
        "address_city": user.address_city,
        "address_state": user.address_state,
        "password":user.password
    }
    return JSONResponse(content=user_dict)

@app.patch("/users/{id}")
def update_user(id: str, user_data: UserCreateUpdateModel):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = user_data.name
    user.age = user_data.age
    user.cpf = user_data.cpf
    user.gender = user_data.gender
    user.email = user_data.email
    user.zipcode = user_data.zipcode
    user.address = user_data.address
    user.address_number = user_data.address_number
    user.address_neighborhood = user_data.address_neighborhood
    user.address_city = user_data.address_city
    user.address_state = user_data.address_state
    user.password = user_data.password

    db.commit()
    db.refresh(user)
    return JSONResponse(content={"message": "Usuário Atualizado com sucesso"})

@app.delete("/users/{id}")
def delete_user(id: str):
    db = SessionLocal()
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(user)
    db.commit()
    return JSONResponse(content={"message": "Usuário deletado com sucesso"})

@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    user_list = []
    for user in users:
        user_dict = {
            "id": str(user.id),
            "name": user.name,
            "age": user.age,
            "cpf": user.cpf,
            "gender": user.gender,
            "email": user.email,
            "zipcode": user.zipcode,
            "address": user.address,
            "address_number": user.address_number,
            "address_neighborhood": user.address_neighborhood,
            "address_city": user.address_city,
            "address_state": user.address_state,
        }
        user_list.append(user_dict)
    return JSONResponse(content={"users": user_list})

