from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Dummy database
menu_items = [
    {'id': 'DRK1', 'name': 'Cafe đen', 'price': 35000},
    {'id': 'DRK2', 'name': 'Cafe sữa', 'price': 35000},
    {'id': 'DRK3', 'name': 'Cafe muối', 'price': 45000},
    {'id': 'DRK4', 'name': 'Hayla cafe', 'price': 48000},
    {'id': 'DRK5', 'name': 'Hayla cafe 2', 'price': 47000},
    {'id': 'DRK6', 'name': 'Cafe Chocolate', 'price': 45000},
    {'id': 'DRK7', 'name': 'Cafe Caramel', 'price': 45000},
    {'id': 'DRK8', 'name': 'Cafe Kem sữa', 'price': 47000},
    {'id': 'DRK10', 'name': 'Trà bưởi', 'price': 47000},
    {'id': 'DRK11', 'name': 'Trà vải lài', 'price': 45000},
    {'id': 'DRK12', 'name': 'Trà nhài đác thơm', 'price': 45000},
    {'id': 'DRK13', 'name': 'Trà đào', 'price': 45000},
    {'id': 'DRK14', 'name': 'Trà tắc xí muội', 'price': 47000},
    {'id': 'DRK15', 'name': 'Trà hoa hồng', 'price': 40000},
    {'id': 'DRK16', 'name': 'Trà sữa thái', 'price': 40000},
    {'id': 'DRK17', 'name': 'Trà lài Machiato', 'price': 40000},
    {'id': 'DRK18', 'name': 'Trà sữa nguyên lá', 'price': 39000},
    {'id': 'DRK19', 'name': 'Trà sữa kem muối', 'price': 43000},
    {'id': 'DRK20', 'name': 'Trà sữa blao lài', 'price': 40000},
    {'id': 'DRK21', 'name': 'Trà sữa ô long sữa', 'price': 40000},
    {'id': 'DRK22', 'name': 'Trà sữa mây', 'price': 42000},
    {'id': 'DRK23', 'name': 'Cafe sữa dừa', 'price': 38000},
    {'id': 'DRK24', 'name': 'Socola sữa dừa', 'price': 47000},
    {'id': 'DRK25', 'name': 'Matcha latte', 'price': 50000},
    {'id': 'DRK26', 'name': 'Trà sen kem dứa', 'price': 50000},
]



class Order(BaseModel):
    item_id: str
    quantity: int


@app.get("/menu")
def get_menu():
    return {"menu": menu_items}


@app.post("/order")
def place_order(lst_order: list[Order]):

    print(lst_order)
    return {"lst_order": lst_order}
