import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString

# 1. 한라산 GeoJSON 로드 (다중 폴리곤 처리용)
hallasan_raw = gpd.read_file("db/data/hallasan.geojson")

# 2. 단일 폴리곤으로 합치기 (unary_union으로)
hallasan_union = hallasan_raw.unary_union  # 단일 MultiPolygon or Polygon

# 3. 경로 데이터 로드
paths_df = pd.read_csv("db\excel\jeju_with_coords_kakao.csv")

paths_df = paths_df.dropna(
    subset=['출발_lat', '출발_lon', '도착_lat', '도착_lon']).copy()

paths_df[['출발_lat', '출발_lon', '도착_lat', '도착_lon']] = paths_df[[
    '출발_lat', '출발_lon', '도착_lat', '도착_lon']].astype(float)

# 4. LineString 생성
paths_df['geometry'] = paths_df.apply(lambda row: LineString([
    (row['출발_lon'], row['출발_lat']),
    (row['도착_lon'], row['도착_lat'])
]), axis=1)
paths_gdf = gpd.GeoDataFrame(paths_df, geometry='geometry', crs="EPSG:4326")

# 5. 교차 여부 필터링
paths_gdf['intersects_hallasan'] = paths_gdf.geometry.intersects(
    hallasan_union)
filtered = paths_gdf[~paths_gdf['intersects_hallasan']].copy()

# 6. 결과 저장
filtered_df = filtered[['출발_lat', '출발_lon', '도착_lat', '도착_lon']]
output_path = "/mnt/data/jeju_paths_avoiding_hallasan.csv"
filtered_df.to_csv(output_path, index=False)

output_path
