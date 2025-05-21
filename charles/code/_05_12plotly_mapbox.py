import pandas as pd
import plotly.graph_objects as go

# 데이터 불러오기
paths_df = pd.read_csv(
    "db/excel/jeju_with_coords_kakao.csv", encoding='utf-8-sig')
paths_df = paths_df.dropna(subset=['출발_lat', '출발_lon', '도착_lat', '도착_lon'])

stations_df = pd.read_csv(
    "db/excel/제주도_충전소_with_coords.csv", encoding='utf-8-sig')
stations_df = stations_df.dropna(subset=['lat', 'lon'])

# # 데이터 확인
# print(f'충전소 위치 :{stations_df.head(3)}')
# print(f'경로 데이터 :{paths_df.head(3)}')

# 결측 제거 및 float 변환
paths_df = paths_df.dropna(
    subset=['출발_lat', '출발_lon', '도착_lat', '도착_lon']).copy()
paths_df[['출발_lat', '출발_lon', '도착_lat', '도착_lon']] = paths_df[[
    '출발_lat', '출발_lon', '도착_lat', '도착_lon']].astype(float)


stations_df = stations_df.dropna(subset=['lat', 'lon']).copy()
stations_df[['lat', 'lon']] = stations_df[['lat', 'lon']].astype(float)

# 중심 좌표 계산
center_lat = (paths_df['출발_lat'].mean() + paths_df['도착_lat'].mean()) / 2
center_lon = (paths_df['출발_lon'].mean() + paths_df['도착_lon'].mean()) / 2

# ✅ 모든 경로를 하나의 trace로 묶기
route_lat = []
route_lon = []

for _, row in paths_df.iterrows():
    route_lat.extend([row['출발_lat'], row['도착_lat'], None])  # None: 선분 분리
    route_lon.extend([row['출발_lon'], row['도착_lon'], None])

# 📊 시각화
fig = go.Figure()

# 이동 경로: 하나의 trace로
fig.add_trace(go.Scattermapbox(
    mode="lines",
    lon=route_lon,
    lat=route_lat,
    line=dict(width=1.5, color='green'),
    name="이동 경로",
    opacity=0.5
))

# 충전소 위치: 마커
fig.add_trace(go.Scattermapbox(
    mode="markers+text",
    lon=stations_df['lon'],
    lat=stations_df['lat'],
    marker=dict(size=8, color='red'),
    text=stations_df['충전소명'],
    name='충전소',
    textposition='top right'
))

# Mapbox 토큰 설정
fig.update_layout(
    mapbox=dict(
        accesstoken="eyJ1IjoicGFtbzIzIiwiYSI6ImNtYWZocTBobzAyZWYya3F4cHRleWo3YjQifQ",
        style="carto-positron",
        center=dict(lat=center_lat, lon=center_lon),
        zoom=10.5
    ),
    title="제주도 EV 경로 + 충전소 분포 (Trace 최적화)",
    height=800,
    margin=dict(l=0, r=0, t=40, b=0)
)

fig.write_html("db/excel/jeju_ev_final_optimized.html")
print("✅ 이동 경로 + 충전소 시각화 완료: jeju_ev_final_optimized.html")
