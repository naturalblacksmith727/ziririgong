import pandas as pd
import numpy as np
import folium
from folium import GeoJson
from shapely.geometry import Point, LineString, shape
from shapely.ops import unary_union
import json

# 1. 데이터 경로 설정 (★ 로컬 PC 경로로 수정 ★)
path_csv_path = "db\최종사용 데이터\jeju_paths_with_reroute_and_chargers.csv"
geojson_path = "db\qgis\mt.hanlla_and_around.geojson"

# 2. 이동 경로 데이터 불러오기
df_paths = pd.read_csv(path_csv_path)

# 필수 좌표 결측치 제거
columns_to_check = ['출발_lat', '출발_lon', '도착_lat', '도착_lon']
df_paths = df_paths.dropna(subset=columns_to_check).copy()

# 3. GeoJSON 불러와 shapely 지오메트리로 병합
with open(geojson_path, "r", encoding="utf-8") as f:
    geo_data = json.load(f)

geometries = [shape(feature["geometry"]) for feature in geo_data["features"]]
hallasan_union = unary_union(geometries)

# 4. 출발/도착/직선 라인 생성
df_paths['출발_point'] = df_paths.apply(
    lambda r: Point(r['출발_lon'], r['출발_lat']), axis=1)
df_paths['도착_point'] = df_paths.apply(
    lambda r: Point(r['도착_lon'], r['도착_lat']), axis=1)
df_paths['direct_line'] = df_paths.apply(
    lambda r: LineString([r['출발_point'], r['도착_point']]), axis=1)

# 5. 한라산을 통과하는 경로만 필터링
intersecting = df_paths[df_paths['direct_line'].apply(
    lambda line: line.intersects(hallasan_union))].copy()

# 6. 우회점 탐색 (한라산 외곽 buffer에서 점 선택)
buffer = hallasan_union.buffer(0.01)
coords = list(buffer.exterior.coords)

rerouted = []
for _, row in intersecting.iterrows():
    for test_lat, test_lon in coords[::len(coords)//30]:  # 30개 샘플링
        mid = Point(test_lon, test_lat)
        l1 = LineString([row['출발_point'], mid])
        l2 = LineString([mid, row['도착_point']])
        if not (l1.intersects(hallasan_union) or l2.intersects(hallasan_union)):
            rerouted.append({
                '출발_lat': row['출발_lat'], '출발_lon': row['출발_lon'],
                '우회_lat': mid.y, '우회_lon': mid.x,
                '도착_lat': row['도착_lat'], '도착_lon': row['도착_lon']
            })
            break

# 7. 시각화
m = folium.Map(location=[33.38, 126.55], zoom_start=11)

# 한라산 경계 시각화
GeoJson(hallasan_union).add_to(m)

# 우회 경로 시각화
for row in rerouted:
    folium.PolyLine(
        locations=[
            [row['출발_lat'], row['출발_lon']],
            [row['우회_lat'], row['우회_lon']],
            [row['도착_lat'], row['도착_lon']]
        ],
        color='blue',
        weight=2,
        opacity=0.8
    ).add_to(m)

# 8. 저장
m.save("HTML/rerouted_paths_via_geojson_final.html")
print("✔ HTML 저장 완료: rerouted_paths_via_geojson_final.html")
