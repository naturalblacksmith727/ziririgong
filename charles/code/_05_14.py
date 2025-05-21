# import pandas as pd
# import numpy as np
# import folium
# from folium.plugins import HeatMap, MarkerCluster
# from scipy.spatial import cKDTree

# # 1. 데이터 불러오기
# df_paths = pd.read_csv(
#     r"C:\Users\charl\OneDrive\Desktop\기타\coding\coding_on_study\ziririgon\First_project\db\최종사용 데이터\jeju_paths_with_reroute_and_chargers.csv")
# df_chargers = pd.read_csv(
#     r"C:\Users\charl\OneDrive\Desktop\기타\coding\coding_on_study\ziririgon\First_project\db\최종사용 데이터\제주도_충전소_with_coords.csv").dropna(subset=['lat', 'lon'])

# # 2. 경로 지점 추출 (출발, 도착, 우회 포함)
# route_points = []
# for _, row in df_paths.iterrows():
#     route_points.append((row['출발_lat'], row['출발_lon']))
#     if not pd.isna(row['우회_lat']):
#         route_points.append((row['우회_lat'], row['우회_lon']))
#     route_points.append((row['도착_lat'], row['도착_lon']))
# df_route_points = pd.DataFrame(route_points, columns=['lat', 'lon'])

# # 3. 충전소 좌표 KDTree 구축
# charger_coords = df_chargers[['lat', 'lon']].values
# tree = cKDTree(charger_coords)

# # 4. 경로 지점별 반경 내 충전소 존재 여부
# radius_deg = 0.009  # 약 1km
# query_coords = df_route_points[['lat', 'lon']].values
# distances, _ = tree.query(query_coords, distance_upper_bound=radius_deg)
# df_route_points['is_covered'] = distances != np.inf

# # 5. 지도 생성
# m = folium.Map(location=[33.38, 126.55], zoom_start=11)

# # 6. 커버된 경로 지점 (파란 히트맵)
# covered_pts = df_route_points[df_route_points['is_covered']]
# HeatMap(
#     covered_pts[['lat', 'lon']].values.tolist(),
#     radius=12,
#     blur=10,
#     min_opacity=0.5,
#     gradient={0.2: 'lightblue', 0.5: 'blue', 1.0: 'navy'}
# ).add_to(m)

# # 7. 미커버 경로 지점 (빨간 히트맵)
# uncovered_pts = df_route_points[~df_route_points['is_covered']]
# HeatMap(
#     uncovered_pts[['lat', 'lon']].values.tolist(),
#     radius=12,
#     blur=10,
#     min_opacity=0.7,
#     gradient={0.2: 'orange', 0.5: 'red', 1.0: 'darkred'}
# ).add_to(m)

# # 8. 충전소 강조 마커 (진한 파란색 + 팝업)
# cluster = MarkerCluster().add_to(m)
# for _, row in df_chargers.iterrows():
#     lat_str = f"{row['lat']:.5f}"
#     lon_str = f"{row['lon']:.5f}"
#     popup_html = f"<b>충전소</b><br>위도: {lat_str}<br>경도: {lon_str}"

#     folium.CircleMarker(
#         location=[row['lat'], row['lon']],
#         radius=6,
#         color='blue',
#         fill=True,
#         fill_color='blue',
#         fill_opacity=0.95,
#         popup=folium.Popup(popup_html, max_width=250)
#     ).add_to(cluster)


# # 9. 저장
# m.save("heatmap_highlighted_charger_edges.html")

# string 수정

import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap, MarkerCluster
from scipy.spatial import cKDTree

# 1. 데이터 불러오기
df_paths = pd.read_csv(
    r"C:\Users\charl\OneDrive\Desktop\기타\coding\coding_on_study\ziririgon\First_project\db\최종사용 데이터\jeju_paths_with_reroute_and_chargers.csv")
df_chargers = pd.read_csv(
    r"C:\Users\charl\OneDrive\Desktop\기타\coding\coding_on_study\ziririgon\First_project\db\최종사용 데이터\제주도_충전소_with_coords.csv").dropna(subset=['lat', 'lon'])

# 2. 경로 지점 추출 (출발, 도착, 우회 포함)
route_points = []
for _, row in df_paths.iterrows():
    route_points.append((row['출발_lat'], row['출발_lon']))
    if not pd.isna(row['우회_lat']):
        route_points.append((row['우회_lat'], row['우회_lon']))
    route_points.append((row['도착_lat'], row['도착_lon']))
df_route_points = pd.DataFrame(route_points, columns=['lat', 'lon'])

# 3. 충전소 좌표 KDTree 구축
charger_coords = df_chargers[['lat', 'lon']].values
tree = cKDTree(charger_coords)

# 4. 경로 지점별 반경 내 충전소 존재 여부
radius_deg = 0.009  # 약 1km
query_coords = df_route_points[['lat', 'lon']].values
distances, _ = tree.query(query_coords, distance_upper_bound=radius_deg)
df_route_points['is_covered'] = distances != np.inf

# 5. 지도 생성
m = folium.Map(location=[33.38, 126.55], zoom_start=11)

# 6. 커버된 경로 지점 (파란 히트맵)
covered_pts = df_route_points[df_route_points['is_covered']]
HeatMap(
    covered_pts[['lat', 'lon']].values.tolist(),
    radius=12,
    blur=10,
    min_opacity=0.5,
    gradient={"0.2": 'lightblue', "0.5": 'blue', "1.0": 'navy'}  # ← 수정된 부분
).add_to(m)

# 7. 미커버 경로 지점 (빨간 히트맵)
uncovered_pts = df_route_points[~df_route_points['is_covered']]
HeatMap(
    uncovered_pts[['lat', 'lon']].values.tolist(),
    radius=12,
    blur=10,
    min_opacity=0.7,
    gradient={"0.2": 'orange', "0.5": 'red', "1.0": 'darkred'}  # ← 수정된 부분
).add_to(m)

# 8. 충전소 강조 마커 (진한 파란색 + 팝업)
cluster = MarkerCluster().add_to(m)
for _, row in df_chargers.iterrows():
    lat_str = f"{row['lat']:.5f}"
    lon_str = f"{row['lon']:.5f}"
    popup_html = f"<b>충전소</b><br>위도: {lat_str}<br>경도: {lon_str}"

    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=6,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.95,
        popup=folium.Popup(popup_html, max_width=250)
    ).add_to(cluster)

# 9. 저장
m.save("heatmap_highlighted_charger_edges.html")
