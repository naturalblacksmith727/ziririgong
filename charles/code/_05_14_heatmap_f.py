import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from scipy.spatial import cKDTree

# 1. 데이터 로드
path_df = pd.read_csv(
    "db/excel/최종사용 데이터/jeju_paths_with_reroute_and_chargers.csv")
charger_df = pd.read_csv(
    "db/excel/최종사용 데이터/제주도_충전소_with_coords.csv").dropna(subset=["lat", "lon"])

# 2. 이동 경로 포인트 추출 (출발, 도착, 우회 포함)
route_points = []
for _, row in path_df.iterrows():
    if not pd.isna(row['출발_lat']) and not pd.isna(row['출발_lon']):
        route_points.append((row['출발_lat'], row['출발_lon']))
    if not pd.isna(row['우회_lat']) and not pd.isna(row['우회_lon']):
        route_points.append((row['우회_lat'], row['우회_lon']))
    if not pd.isna(row['도착_lat']) and not pd.isna(row['도착_lon']):
        route_points.append((row['도착_lat'], row['도착_lon']))

df_route_points = pd.DataFrame(route_points, columns=['lat', 'lon'])

# 3. 충전소 KDTree 기반 커버 여부 판단
charger_coords = charger_df[['lat', 'lon']].values
tree = cKDTree(charger_coords)

query_coords = df_route_points[['lat', 'lon']].values
radius_deg = 0.009  # 위도 기준 약 1km
distances, _ = tree.query(query_coords, distance_upper_bound=radius_deg)
df_route_points['is_covered'] = distances != np.inf

# 4. 좌표 정제 함수 (folium 오류 방지용)


def safe_coord_list(df):
    coords = []
    for lat, lon in df[['lat', 'lon']].values:
        if (
            isinstance(lat, float) and isinstance(lon, float) and
            not np.isnan(lat) and not np.isnan(lon)
        ):
            coords.append([lat, lon])
    return coords


route_coords_list = safe_coord_list(df_route_points)
charger_coords_list = safe_coord_list(charger_df)

# 5. 지도 생성
m = folium.Map(location=[33.38, 126.55], zoom_start=11)

# 🔷 충전소 히트맵
HeatMap(
    charger_coords_list,
    radius=14,
    blur=8,
    min_opacity=0.3,
    gradient={0.2: 'cyan', 0.5: 'deepskyblue', 0.8: 'blue', 1.0: 'darkblue'}
).add_to(m)

# 🔴 EV 이동 경로 히트맵
HeatMap(
    route_coords_list,
    radius=14,
    blur=5,
    min_opacity=0.5,
    gradient={0.2: 'yellow', 0.5: 'orange', 0.8: 'red', 1.0: 'darkred'}
).add_to(m)

# 6. 저장
m.save("db/excel/최종사용 데이터/heatmap_with_routes_and_charger_density.html")
