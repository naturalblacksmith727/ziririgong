import folium
from folium.plugins import HeatMap
import pandas as pd

# CSV 파일 로드
df = pd.read_csv("jeju_with_coords_kakao.csv", encoding='utf-8-sig')

# # 지도 중심: 제주도
# jeju_map = folium.Map(location=[33.38, 126.55], zoom_start=11)

# # 🔴 출발지 히트맵 (빨간색 계열)
# start_points = df[['출발_lat', '출발_lon']].dropna().values.tolist()
# HeatMap(start_points, radius=8, gradient={
#         0.4: 'orange', 0.65: 'red', 1: 'darkred'}).add_to(jeju_map)

# # 🔵 도착지 히트맵 (파란색 계열)
# end_points = df[['도착_lat', '도착_lon']].dropna().values.tolist()
# HeatMap(end_points, radius=8, gradient={
#         0.4: 'lightblue', 0.65: 'blue', 1: 'darkblue'}).add_to(jeju_map)

# # 🟢 출발→도착 경로선 (궤적 시각화)
# for _, row in df.dropna(subset=['출발_lat', '출발_lon', '도착_lat', '도착_lon']).iterrows():
#     folium.PolyLine(
#         [(row['출발_lat'], row['출발_lon']), (row['도착_lat'], row['도착_lon'])],
#         color="green", weight=1, opacity=0.5
#     ).add_to(jeju_map)

# # HTML 저장
# jeju_map.save("jeju_ev_station_heatmap.html")
# print("✅ 시각화 HTML 저장 완료: jeju_ev_station_heatmap.html")

print(df.dtypes)
print(df.head())
