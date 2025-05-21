import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
import geopandas as gpd
from tqdm import tqdm
import folium


# 1. 데이터 불러오기
paths_df = pd.read_csv("db\excel\jeju_with_coords_kakao.csv")
hallasan = gpd.read_file("db\qgis\국립공원공단_국립공원 공원경계_20231231\hallasan.geojson")
hallasan_union = hallasan.unary_union

# 2. 한라산 내부를 통과하는 경로 필터링
paths_df['출발_point'] = paths_df.apply(
    lambda r: Point(r['출발_lon'], r['출발_lat']), axis=1)
paths_df['도착_point'] = paths_df.apply(
    lambda r: Point(r['도착_lon'], r['도착_lat']), axis=1)
paths_df['direct_line'] = paths_df.apply(
    lambda r: LineString([r['출발_point'], r['도착_point']]), axis=1)
hallasan_paths = paths_df[paths_df['direct_line'].apply(
    lambda line: line.intersects(hallasan_union))].copy()

# 3. 접점 수 계산 함수


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
        return len(inter.geoms) * 2
    return 2

# 4. 회피점 찾기 함수


def find_valid_bypass_point(start, end, polygon, max_attempts=10, initial_buffer=0.02, buffer_step=0.01):
    for i in range(max_attempts):
        buffer_dist = initial_buffer + i * buffer_step
        temp_buffer = polygon.buffer(buffer_dist)
        coords = list(temp_buffer.exterior.coords)
        for candidate in coords[::len(coords)//100]:
            mid = Point(candidate)
            l1 = LineString([start, mid])
            l2 = LineString([mid, end])
            if count_intersections(l1, polygon) <= 1 and count_intersections(l2, polygon) <= 1:
                return mid, buffer_dist
    return None, None


# 5. 회피 경로 계산
rerouted_records = []
buffer_start = 0.02
buffer_step = 0.01

for _, row in tqdm(hallasan_paths.iterrows(), total=len(hallasan_paths)):
    sp = row['출발_point']
    ep = row['도착_point']
    direct_line = LineString([sp, ep])
    if count_intersections(direct_line, hallasan_union) <= 1:
        continue

    valid_pt, used_buf = find_valid_bypass_point(sp, ep, hallasan_union,
                                                 initial_buffer=buffer_start,
                                                 buffer_step=buffer_step)
    if valid_pt:
        rerouted_records.append({
            '출발_lat': sp.y,
            '출발_lon': sp.x,
            '도착_lat': ep.y,
            '도착_lon': ep.x,
            '우회_lat': valid_pt.y,
            '우회_lon': valid_pt.x,
            '사용버퍼': used_buf
        })

rerouted_df = pd.DataFrame(rerouted_records)
rerouted_df.to_csv("db\excel\hallasan_rerouted_paths.csv", index=False)

# 6. Folium HTML 지도 시각화
m = folium.Map(location=[33.36, 126.53], zoom_start=10)

for _, row in rerouted_df.iterrows():
    folium.PolyLine([
        [row['출발_lat'], row['출발_lon']],
        [row['우회_lat'], row['우회_lon']],
        [row['도착_lat'], row['도착_lon']]
    ], color='red', weight=2.5).add_to(m)

m.save("db\excel\hallasan_rerouted_paths2.html")
