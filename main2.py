from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from databases import Database

# PostgreSQL 연결 정보 (자신에 맞게 수정)
DATABASE_URL = "postgresql://postgres:@@lc717283@localhost:5432/results"

# 데이터베이스 연결
database = Database(DATABASE_URL)
app = FastAPI()

# CORS 설정 (React 앱에서 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 앱 시작 시 데이터베이스 연결
@app.on_event("startup")
async def startup():
    await database.connect()

# 앱 종료 시 데이터베이스 연결 해제
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# API 엔드포인트 - 상위 10개 데이터 조회
@app.get("/swim_rank")
async def read_swim_rank():
    query = "SELECT * FROM swim_rank LIMIT 10"
    results = await database.fetch_all(query)
    return results
