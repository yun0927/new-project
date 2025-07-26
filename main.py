from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

# 안쓰는 파일
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 단계에서는 * 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CSV 로드 및 전처리
df = pd.read_csv("C:/Users/yyjeo/Desktop/new/final.csv")
df.columns = df.columns.str.strip().str.lower()

# 문자열 칼럼 정리
df['gender'] = df['gender'].str.strip().str.lower()
df['age'] = df['age'].str.strip().str.lower()
df['event'] = df['event'].str.strip().str.lower()

class PredictionInput(BaseModel):
    gender: str
    age: str        # "25-29" 형태
    record: float   # 초 단위 기록
    event: str

@app.post("/predict")
def predict_rank(input: PredictionInput):
    # 입력값 정리
    gender = input.gender.strip().lower()
    age = input.age.strip().lower()
    event = input.event.strip().lower()

    # 🔍 입력 확인
    print("=== 입력값 ===")
    print("gender:", gender)
    print("age:", age)
    print("event:", event)
    print("record:", input.record)
    print()

    # 🔍 유니크 값 확인
    print("=== 유니크 값 확인 (df) ===")
    print("df['gender'].unique():", df['gender'].unique())
    print("df['age'].unique():", df['age'].unique())
    print("df['event'].unique():", df['event'].unique())
    print()

    # 🔍 조건 필터링
    group = df[
        (df['gender'] == gender) &
        (df['age'] == age) &
        (df['event'] == event)
    ]

    print(f"=== 필터링된 데이터 수: {len(group)}명 ===")
    if not group.empty:
        print(group[['gender', 'age', 'event', 'time_sec']].head(10))
    print()

    # 예외 처리
    if group.empty:
        return {
            "message": f"'{age}' 그룹의 '{gender.upper()}', '{event}' 기록이 없습니다."
        }

    # 순위 계산
    rank = (group['time_sec'] < input.record).sum() + 1
    return {
        "predicted_rank": int(rank),
        "total_participants": len(group)
    }
