import pandas as pd
import matplotlib.pyplot as plt

# 1. CSV 불러오기
df = pd.read_csv("C:/Users/yyjeo/desktop/results_with_seconds.csv")
df.columns = df.columns.str.strip().str.lower()

# 2. 🆕 year 컬럼 생성: 30개씩 묶어서 2020~2024년 분배
df['year'] = [2020 + i // 30 for i in range(len(df))]

# 3. 사용자 입력
user_gender = input("성별을 입력하세요 (M/F): ").strip().upper()
user_age_input = int(input("당신의 나이를 입력하세요 (예: 22): ").strip())
user_record = float(input("당신의 기록을 초 단위로 입력하세요 (예: 28.50): ").strip())

# 4. 나이를 연령대 범위로 변환 (5세 단위)
def get_age_group(age):
    start = (age // 5) * 5
    return f"{start}-{start+4}"

user_age_group = get_age_group(user_age_input)

print(f"\n📌 자동 매핑된 연령대: {user_age_group}")

# 5. 필터링
filtered = df[(df['gender'] == user_gender) & (df['age'] == user_age_group)]

# 6. 연도별 순위 예측
year_rank = {}
for year in sorted(filtered['year'].unique()):
    year_data = filtered[filtered['year'] == year]
    faster_count = (year_data['time_sec'] < user_record).sum()
    rank = faster_count + 1
    year_rank[year] = rank

# 7. 결과 출력
print("\n📊 예측 순위:")
for year, rank in year_rank.items():
    print(f"{year}년 → {rank}위")

# 8. 시각화
plt.figure(figsize=(8, 5))
plt.plot(list(year_rank.keys()), list(year_rank.values()), marker='o', linestyle='-', color='blue')
plt.gca().invert_yaxis()
plt.title(f"{user_age_group}세 {user_gender} 사용자 기록 {user_record}초의 연도별 예상 순위")
plt.xlabel("연도")
plt.ylabel("예상 순위")
plt.grid(True)
plt.tight_layout()
plt.show()





