import pandas as pd

# 1. 전체 충전소 정보 CSV 불러오기
df = pd.read_csv("충전소_전체정보.csv", encoding="utf-8-sig")
# 한국어는 무조건 utf-8 하는게 중요, 한컴은 또 다름 ;;
# 여기서 utf-8-sig 와 utf-8 차이점은
# https://yeongwoo-cho.tistory.com/entry/UTF-8%EA%B3%BC-UTF-8-sig-%EC%9D%98-%EC%B0%A8%EC%9D%B4%EC%A0%90 잘 정리되어 있음


print(df.head())  # df 잘 불러왔는지 확인

print(df['주소'].values)  # 주소만 빼올수 있는거 확인

# 2. 필터링: 주소에 '서울'과 '강남'이 모두 포함된 경우만
filtered = df[df["주소"].str.contains(
    "서울", na=False) & df["주소"].str.contains("강남", na=False)]

# 3. 결과 확인
print(f" 필터링된 충전소 수: {len(filtered)}건")

# 4. 새 CSV로 저장
filtered.to_csv("제주도_충전소.csv", index=False, encoding="utf-8-sig")
print(" '제주도_충전소.csv' 저장")

# # ex 전체 중 '제주' 지역만
# filtered = df[df["주소"].str.contains("제주", na=False)]

# # 예: '세종' 포함하고 '고속도로' 포함하는 충전소만
# filtered = df[df["주소"].str.contains(
#     "세종", na=False) & df["상세주소"].str.contains("고속도로", na=False)]
