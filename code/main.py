from fastapi import FastAPI
from typing import List  # ネストされたBodyを定義するために必要
from starlette.middleware.cors import CORSMiddleware  # CORSを回避するために必要
from db import session  # DBと接続するためのセッション
from model import UserTable, User, ItemsTable, Item  # 今回使うモデルをインポート

app = FastAPI()

# CORSを回避するために設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------APIの定義------------
# テーブルにいる全ユーザ情報を取得 GET
@app.get("/users")
def read_users():
    users = session.query(UserTable).all()
    return users


@app.get("/items")
def read_items():
    items = session.query(ItemsTable).all()
    return items


@app.get("/items/barcode")
def read_item(barcode: str):
    item = session.query(ItemsTable).filter(ItemsTable.barcode == barcode).first()
    return item


@app.get("/items/name")
def read_name(name: str):
    search = "%{}%".format(name)
    item = session.query(ItemsTable).filter(ItemsTable.like(search)).all()
    return item


@app.get("/items/company")
def read_name(company: str):
    item = session.query(ItemsTable).filter(ItemsTable.company == company).first()
    return item


# idにマッチするユーザ情報を取得 GET
@app.get("/users/{user_id}")
def read_user(user_id: int):
    user = session.query(UserTable).filter(UserTable.id == user_id).first()
    return user


# ユーザ情報を登録 POST
@app.post("/user")
# クエリでnameとstrを受け取る
# /user?name="三郎"&age=10
async def create_user(name: str, age: int):
    user = UserTable()
    user.name = name
    user.age = age
    session.add(user)
    session.commit()


@app.post("/item")
# クエリでnameとstrを受け取る
# /user?name="三郎"&age=10
async def create_item(name: str, barcode: str, category: str, price: str):
    item = ItemsTable()
    item.name = name
    item.category = category
    item.barcode = barcode
    item.price = price
    session.add(item)
    session.commit()


# 複数のユーザ情報を更新 PUT
@app.put("/users")
# modelで定義したUserモデルのリクエストbodyをリストに入れた形で受け取る
# users=[{"id": 1, "name": "一郎", "age": 16},{"id": 2, "name": "二郎", "age": 20}]
async def update_users(users: List[User]):
    for new_user in users:
        user = session.query(UserTable).filter(UserTable.id == new_user.id).first()
        user.name = new_user.name
        user.age = new_user.age
        session.commit()


@app.put("/item")
async def update_items(users: List[Item]):
    for new_item in users:
        item = session.query(ItemsTable).filter(ItemsTable.id == new_item.id).first()
        item.name = new_item.name
        item.category = new_item.category
        item.barcode = new_item.barcode

        session.commit()
