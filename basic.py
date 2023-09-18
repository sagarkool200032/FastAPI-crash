from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory = {
        
        }
# GET REQ
@app.get("/")
def home ():
    return {"Data": "Test"}

@app.get("/about")
def about ():
    return {"Data": "About"}

# Path Parameter
@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(description="The ID of the user",gt=0)):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID not found.")
    return inventory[item_id]

# Path and Search/Query Parameter
@app.get("/get-by-name")
def get_item(name: str):
    for item_id in inventory:
        if inventory[item_id].name == name: return inventory[item_id]
    raise HTTPException(status_code=404, detail="Item name not found.")
# @app.get("/get-by-name/{item_id}")
# def get_item(item_id: int,test: int, name: Optional[str] =  None):
#     for item_id in inventory:
#         if inventory[item_id].name == name: return inventory[item_id]
#     return {"Data": "Not found"}

# Post Req
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=404, detail="Item ID already exists.")

    inventory[item_id] = item
    return inventory[item_id]

# Update Req
@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exists.")
    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]

# Delete Request
@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="ID of the item")):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exists")
    return {"Success": "Item deleted!"}