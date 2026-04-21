from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="FastAPI 기본 예제", version="1.0.0")

# --- Pydantic 모델 ---
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

class User(BaseModel):
    username: str
    email: str
    age: Optional[int] = None

# --- 간단한 인메모리 DB ---
fake_db: dict[int, dict] = {
    1: {"name": "사과", "price": 1000.0, "is_offer": False},
    2: {"name": "바나나", "price": 500.0, "is_offer": True},
}

# --- GET: 루트 ---
@app.get("/")
def read_root():
    return {"message": "FastAPI 서버가 정상 동작 중입니다!"}

# --- GET: 경로 파라미터 + 쿼리 파라미터 ---
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    item = fake_db[item_id]
    if q:
        item["search_query"] = q
    return item

# --- GET: 전체 목록 조회 ---
@app.get("/items")
def list_items():
    return fake_db

# --- POST: 아이템 생성 ---
@app.post("/items/{item_id}", status_code=201)
def create_item(item_id: int, item: Item):
    if item_id in fake_db:
        raise HTTPException(status_code=400, detail="이미 존재하는 ID입니다")
    fake_db[item_id] = item.model_dump()
    return {"message": "생성 완료", "item_id": item_id, "item": item}

# --- PUT: 아이템 수정 ---
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    fake_db[item_id] = item.model_dump()
    return {"message": "수정 완료", "item_id": item_id, "item": item}

# --- DELETE: 아이템 삭제 ---
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    del fake_db[item_id]
    return {"message": f"ID {item_id} 삭제 완료"}

# --- POST: Request Body 예제 (유저 생성) ---
@app.post("/users")
def create_user(user: User):
    return {"message": "유저 생성 완료", "user": user}


# 직접 실행 시 uvicorn으로 서버 시작
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("06_fast_api:app", host="0.0.0.0", port=8000, reload=True)
