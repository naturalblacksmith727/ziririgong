import pandas as pd
import numpy as np
import folium
from shapely.geometry import Point, LineString
from shapely.affinity import scale
from shapely.geometry import mapping
from folium.plugins import HeatMap
from shapely.geometry import LineString
from scipy.spatial import cKDTree

# 1. 데이터 로드
df_all = pd.read_csv("C:\\Users\\charl\\OneDrive\\Desktop\\기타\\coding\\coding_on_study\\ziririgon\\First_project\\db\\최종사용 데이터\\jeju_with_coords_kakao.csv").dropna(
    subset=['출발_lat', '출발_lon', '도착_lat', '도착_lon'])


# 2. 타원형 회피 경계 정의
center = Point(126.55, 33.368)  # 중심 약간 아래로 이동한 위치
circle = center.buffer(0.0825, resolution=80)  # 반지름 약 9.15km
ellipse = scale(circle, xfact=2.0, yfact=0.75, origin=center)  # 타원 비율 조정

# 3. 교차 판단 함수


def count_intersections(line, polygon):
    inter = line.intersection(polygon)
    if inter.is_empty:
        return 0
    if inter.geom_type == 'Point':
        return 1
    if inter.geom_type == 'MultiPoint':
        return len(inter.geoms)
    if inter.geom_type == 'LineString':
        return 2
    if inter.geom_type == 'MultiLineString':
        return sum(1 for g in inter.geoms if g.length > 0)
    return 3

# 4. 회피점 탐색 함수


def find_valid_random_midpoint(start, end, barrier, max_attempts=20, initial_buffer=0.005, step=0.003, samples=100):
    for i in range(max_attempts):
        dist = initial_buffer + i * step
        buffer_ring = barrier.buffer(dist).exterior
        candidate_pts = list(buffer_ring.coords)[
            ::max(1, len(buffer_ring.coords)//samples)]
        for pt in candidate_pts:
            mid = Point(pt)
            l1, l2 = LineString([start, mid]), LineString([mid, end])
            if count_intersections(l1, barrier) <= 1 and count_intersections(l2, barrier) <= 1:
                return mid, dist
    return None, None


# 5. 전체 경로 처리
records = []
for _, row in df_all.iterrows():
    sp = Point(row['출발_lon'], row['출발_lat'])
    ep = Point(row['도착_lon'], row['도착_lat'])
    direct = LineString([sp, ep])

    if not direct.intersects(ellipse):
        records.append({
            '출발_lat': sp.y, '출발_lon': sp.x,
            '도착_lat': ep.y, '도착_lon': ep.x,
            '우회_lat': None, '우회_lon': None,
            '우회_성공': False, '비고': '경계 외'
        })
        continue

    mid, dist = find_valid_random_midpoint(sp, ep, ellipse)
    if mid:
        records.append({
            '출발_lat': sp.y, '출발_lon': sp.x,
            '도착_lat': ep.y, '도착_lon': ep.x,
            '우회_lat': mid.y, '우회_lon': mid.x,
            '우회_성공': True,
            '비고': f'Buffer={dist:.5f}'
        })
    else:
        records.append({
            '출발_lat': sp.y, '출발_lon': sp.x,
            '도착_lat': ep.y, '도착_lon': ep.x,
            '우회_lat': None, '우회_lon': None,
            '우회_성공': False,
            '비고': '우회 실패'
        })

# 6. 데이터프레임 저장
reroute_df = pd.DataFrame(records)
reroute_df.to_csv("rerouted_elliptical_paths_all.csv", index=False)

# CSV로 저장
pd.DataFrame(records).to_csv(
    "C:\\Users\\charl\\OneDrive\\Desktop\\기타\\coding\\coding_on_study\\ziririgon\\First_project\\_5_17\\ju_paths_with_reroute_combined.csv", index=False)
print("✅ 전체 경로 우회 포함 CSV 저장 완료 → ju_paths_with_reroute_combined.csv")

# 7. 지도 시각화
m = folium.Map(location=[33.38, 126.55], zoom_start=11)

# 회피 경계 시각화
# folium.GeoJson(
#     data={"type": "Feature", "geometry": mapping(ellipse)},
#     name="타원 회피 경계",
#     style_function=lambda x: {"color": "black",
#                               "weight": 2, "fillOpacity": 0.1}
# ).add_to(m)

# 경로 표시 (모두 파란색)
for _, row in reroute_df.iterrows():
    sp = [row['출발_lat'], row['출발_lon']]
    ep = [row['도착_lat'], row['도착_lon']]

    if row['우회_성공']:
        mid = [row['우회_lat'], row['우회_lon']]
        folium.PolyLine([sp, mid, ep], color="blue",
                        weight=2.5, opacity=0.9).add_to(m)
    else:
        folium.PolyLine([sp, ep], color="blue", weight=2.5,
                        opacity=0.6).add_to(m)

# 저장
m.save("rerouted_paths_all_blue.html")
print("🗺️ 지도 저장 완료: rerouted_paths_all_blue.html")

# 충전소랑 합치기

# 충전소 파일 로드
charger_df = pd.read_csv("C:\\Users\\charl\\OneDrive\\Desktop\\기타\\coding\\coding_on_study\\ziririgon\\First_project\\db\\최종사용 데이터\\제주도_충전소_with_coords.csv").dropna(
    subset=["lat", "lon"])

#  충전소 시각화 (빨간색 점)
for _, row in charger_df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=3,
        color='red',
        fill=True,
        fill_opacity=0.9
    ).add_to(m)

m.save("C:\\Users\\charl\\OneDrive\\Desktop\\기타\\coding\\coding_on_study\\ziririgon\\First_project\\_5_17\\rerouted_paths_with_chargers.html")
print("✅ HTML 파일 저장 완료: rerouted_paths_with_chargers.html")

# 경로 + 우회 여부 포함된 CSV (전체 경로)
df = pd.read_csv(
    "C:\\Users\\charl\\OneDrive\\Desktop\\기타\\coding\\coding_on_study\\ziririgon\\First_project\\_5_17\\rerouted_elliptical_paths_all.csv")

# 충전소 위치 CSV
chargers = pd.read_csv("C:\\Users\\charl\\OneDrive\\Desktop\\기타\\coding\\coding_on_study\\ziririgon\\First_project\\db\\최종사용 데이터\\제주도_충전소_with_coords.csv").dropna(
    subset=["lat", "lon"])

# 경로 + 우회 여부 포함된 CSV (전체 경로)
df = pd.read_csv(
    "C:\\Users\\charl\\OneDrive\\Desktop\\기타\\coding\\coding_on_study\\ziririgon\\First_project\\_5_17\\rerouted_elliptical_paths_all.csv")

# 충전소 위치 CSV
chargers = pd.read_csv("C:\\Users\\charl\\OneDrive\\Desktop\\기타\\coding\\coding_on_study\\ziririgon\\First_project\\db\\최종사용 데이터\\제주도_충전소_with_coords.csv").dropna(
    subset=["lat", "lon"])

# 3. 좌표 정제
route_points = [
    [float(lat), float(lon)]
    for lat, lon in route_points
    if pd.notna(lat) and pd.notna(lon)
]

charger_coords = [
    [float(row['lat']), float(row['lon'])]
    for _, row in chargers.iterrows()
    if pd.notna(row['lat']) and pd.notna(row['lon'])
]
# 4. KDTree 생성
charger_tree = cKDTree(charger_coords)

# 5. 각 경로에 대해 가장 가까운 충전소 찾기


def find_nearest_charger(route_point):
    dist, index = charger_tree.query(route_point)
    return charger_coords[index], dist


# 4. 지도 생성 및 히트맵 추가
m = folium.Map(location=[33.38, 126.55], zoom_start=11)

HeatMap(route_points, radius=10, blur=5, min_opacity=0.3,
        gradient={0.2: 'lightblue', 0.5: 'blue', 0.8: 'navy'}).add_to(m)

HeatMap(charger_coords, radius=12, blur=6, min_opacity=0.4,
        gradient={0.2: 'pink', 0.5: 'red', 0.9: 'darkred'}).add_to(m)
