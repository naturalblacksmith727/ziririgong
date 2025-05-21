import pandas as pd


paths_df = pd.read_csv(
    "db/excel/jeju_with_coords_kakao.csv", encoding='utf-8-sig')
paths_df = paths_df.dropna(subset=['출발_lat', '출발_lon', '도착_lat', '도착_lon'])


# 경로 필터링 기준 정의
def is_in_jeju(lat, lon):
    return 33.05 <= lat <= 33.60 and 126.10 <= lon <= 126.95


# 출발지와 도착지 모두 제주도 안에 있는 경우만 남김
mask = paths_df.apply(
    lambda row: is_in_jeju(row['출발_lat'], row['출발_lon']) and is_in_jeju(
        row['도착_lat'], row['도착_lon']),
    axis=1
)
paths_df = paths_df[mask].reset_index(drop=True)

# 파일 csv저장
save_path = r"C:\Users\charl\OneDrive\Desktop\기타\coding\coding_on_study\ziririgon\First_project\db\jeju_with_coords_kakao.csv"
paths_df.to_csv(save_path, index=False, encoding='utf-8-sig')
print(f"✅ 저장 완료: {save_path}")
