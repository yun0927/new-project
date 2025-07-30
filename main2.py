from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import databases
import sqlalchemy

# PostgreSQL DB 연결 설정
DATABASE_URL = "postgresql://postgres:@@lc717283@localhost:5432/postgres"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/predict_rank")
async def predict_rank(
    gender: str = Query(..., description="성별: M 또는 F"),
    age: str = Query(..., description="연령대 예: 20-24"),
    event: str = Query(..., description="종목 예: freestyle"),
    time_sec: float = Query(..., description="기록(초 단위, 예: 31.5)")
):
    # 해당 조건에 맞는 기록을 모두 불러와서 시간순으로 정렬
    query = """
    SELECT time_sec
    FROM swim_rank
    WHERE gender = :gender AND age = :age AND event = :event
    ORDER BY time_sec ASC
    """
    rows = await database.fetch_all(query, values={"gender": gender, "age": age, "event": event})
    
    times = [row["time_sec"] for row in rows]

    # 순위 계산: 나보다 빠른 시간 개수 + 1
    rank = sum(1 for t in times if t < time_sec) + 1

    return {
        "predicted_rank": rank,
        "total_participants": len(times) + 1,
        "your_time": time_sec,
        "gender": gender,
        "age": age,
        "event": event
    }
