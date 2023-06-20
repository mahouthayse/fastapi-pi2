from fastapi import FastAPI, status
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite://todo.db")
Base = declarative_base()
Base.metadata.create_all(engine)
app = FastAPI()

@app.get("/")
def root():
    return "root"
@app.post("/todo", status_code=201)
def create_todo():
    return "create todo item"

@app.get("/todo/{id}")
def read_todo(id: int):
    return "read todo item with id {id}"
@app.put("/todo/{id}")
def update_todo(id: int):
    return "update todo item"
@app.delete("/todo/{id}", status_code=status.HTTP_200_OK)
def delete_todo(id: int):
    return "delete todo item"
@app.get("/todo")
def read_todo_list():
    return "read todo list"

