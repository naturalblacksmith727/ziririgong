# 필요한 라이브러리 불러오기
import pandas as pd
import json
from shapely.geometry import shape, LineString
from shapely.ops import unary_union

#  1. 한라산 GeoJSON 파일 불러오기
with open("db\qgis\국립공원공단_국립공원 공원경계_20231231\hallasan.geojson", "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

# 모든 geometry를 shapely 객체로 변환
hallasan_shapes = [shape(feature["geometry"])
                   for feature in geojson_data["features"]]

# 하나의 다각형 또는 multipolygon으로 통합
hallasan_union = unary_union(hallasan_shapes)

#  2. EV 이동 경로 데이터 불러오기
paths_df = pd.read_csv("db\excel\jeju_with_coords_kakao.csv")

# 결측값 제거 및 타입 변환
paths_df = paths_df.dropna(
    subset=['출발_lat', '출발_lon', '도착_lat', '도착_lon']).copy()

paths_df[['출발_lat', '출발_lon', '도착_lat', '도착_lon']] = paths_df[[
    '출발_lat', '출발_lon', '도착_lat', '도착_lon'
]].astype(float)

# 3. 각 출발-도착을 선(LineString)으로 변환
paths_df['geometry'] = paths_df.apply(lambda row: LineString([
    (row['출발_lon'], row['출발_lat']),
    (row['도착_lon'], row['도착_lat'])
]), axis=1)

# 4. 한라산을 통과하는지 검사
paths_df['intersects_hallasan'] = paths_df['geometry'].apply(
    lambda geom: geom.intersects(hallasan_union)
)

# 5. 한라산을 통과하는 경로만 필터링
hallasan_crossing = paths_df[paths_df['intersects_hallasan']].copy()

# 6. 필요한 열만 저장
hallasan_crossing[['출발_lat', '출발_lon', '도착_lat', '도착_lon']].to_csv(
    "paths_crossing_hallasan.csv", index=False
)


# # 1. 한라산 경계 불러오기
# hallasan_shapes = [shape(feature["geometry"])
#                    for feature in geojson_data["features"]]
# hallasan_union = unary_union(hallasan_shapes)

# # 2. 출발/도착 좌표를 기반으로 LineString 경로 생성
# paths_df['geometry'] = paths_df.apply(lambda row: LineString([
#     (row['출발_lon'], row['출발_lat']),
#     (row['도착_lon'], row['도착_lat'])
# ]), axis=1)

# # 3. 해당 경로가 한라산 경계와 교차하는지 검사
# paths_df['intersects_hallasan'] = paths_df['geometry'].apply(
#     lambda geom: geom.intersects(hallasan_union))

# # 4. 통과하는 경로만 필터링 후 저장
# hallasan_crossing_paths = paths_df[paths_df['intersects_hallasan']]
