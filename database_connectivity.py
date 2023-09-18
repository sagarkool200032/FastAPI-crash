import collections
import contextlib
import logging.config
import sqlite3
import typing
from uuid import UUID

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel
# from pydantic_settings import BaseSettings

class Item(BaseModel):
    name: str
    description: str

app = FastAPI()

def create_database():
    conn = sqlite3.connect("mydatabase.db")  # Replace with your desired database file name
    cursor = conn.cursor()

    # Create a table (replace "items" and column names with your desired table structure)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT
        )
    ''')
    conn.execute("insert into items values(1,'bread','expired');")

    conn.commit()
    conn.close()

# create_database()

def get_db():
    with contextlib.closing(sqlite3.connect("mydatabase.db")) as db:
        db.row_factory = sqlite3.Row
        yield db

@app.get("/items")
def list_books(db: sqlite3.Connection = Depends(get_db)):
    items = db.execute("SELECT * FROM items")
    return {"items": items.fetchall()}

@app.get("/items/{id}")
def retrieve_book(
    id: int, response: Response, db: sqlite3.Connection = Depends(get_db)
):
    cur = db.execute("SELECT * FROM items WHERE id = ? LIMIT 1", [id])
    items = cur.fetchall()
    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return {"items": items}

@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_book(
    item: Item, response: Response, db: sqlite3.Connection = Depends(get_db)
):
    b = dict(item)
    try:
        cur = db.execute(
            """
            INSERT INTO items(name, description)
            VALUES(:name, :description)
            """,
            b,
        )
        db.commit()
    except sqlite3.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)},
        )
    b["id"] = cur.lastrowid
    response.headers["Location"] = f"/books/{b['id']}"
    return b
