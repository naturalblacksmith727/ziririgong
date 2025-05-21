import pandas as pd
import json
import folium
from shapely.geometry import shape, Point, LineString
from shapely.ops import unary_union
from shapely.prepared import prep
from tqdm import tqdm

# 1. 파일 경로 설정 (★ 본인 경로에 맞게 수정)
csv_path = "db/최종사용 데이터/jeju_with_coords_kakao.csv"
geojson_path = "db/qgis/mt.hanlla_and_around.geojson"

# 2. 한라산 GeoJSON 병합 및 준비
with open(geojson_path, "r", encoding="utf-8") as f:
    geo = json.load(f)
geometries = [shape(feat["geometry"]) for feat in geo["features"]]
hallasan_union = unary_union(geometries)
prepared_hallasan = prep(hallasan_union)

# 3. 경로 데이터 불러오기
df = pd.read_csv(csv_path).dropna(
    subset=["출발_lat", "출발_lon", "도착_lat", "도착_lon"])
df["출발_point"] = df.apply(lambda r: Point(r["출발_lon"], r["출발_lat"]), axis=1)
df["도착_point"] = df.apply(lambda r: Point(r["도착_lon"], r["도착_lat"]), axis=1)
df["direct_line"] = df.apply(lambda r: LineString(
    [r["출발_point"], r["도착_point"]]), axis=1)

# 4. 한라산 통과 경로만 필터링
df_intersect = df[df["direct_line"].apply(prepared_hallasan.intersects)].copy()

# 5. 우회 경로 계산
print("🚧 한라산 회피 경로 생성 중...")
rerouted = []
reroute_cache = {}
buffer_start = 0.01
buffer_step = 0.005
max_attempts = 10

for _, row in tqdm(df_intersect.iterrows(), total=len(df_intersect)):
    sp, ep = row["출발_point"], row["도착_point"]
    key = (sp.x, sp.y, ep.x, ep.y)
    if key in reroute_cache:
        result = reroute_cache[key]
        if result:
            rerouted.append(result)
        continue

    reroute_found = False
    for i in range(max_attempts):
        buffer = hallasan_union.buffer(buffer_start + i * buffer_step)
        coords = list(buffer.exterior.coords)

        for lat, lon in coords[::len(coords)//50]:
            mid = Point(lon, lat)
            l1, l2 = LineString([sp, mid]), LineString([mid, ep])

            if not prepared_hallasan.intersects(l1) and not prepared_hallasan.intersects(l2):
                result = {
                    "출발_lat": sp.y, "출발_lon": sp.x,
                    "우회_lat": mid.y, "우회_lon": mid.x,
                    "도착_lat": ep.y, "도착_lon": ep.x,
                    "buffer_used": buffer_start + i * buffer_step
                }
                rerouted.append(result)
                reroute_cache[key] = result
                reroute_found = True
                break
        if reroute_found:
            break
    else:
        reroute_cache[key] = None

# 6. 시각화
print("🗺 지도 시각화 중...")
m = folium.Map(location=[33.38, 126.55], zoom_start=11)
folium.GeoJson(hallasan_union, name="hallasan").add_to(m)

for row in rerouted:
    folium.PolyLine(
        locations=[
            [row["출발_lat"], row["출발_lon"]],
            [row["우회_lat"], row["우회_lon"]],
            [row["도착_lat"], row["도착_lon"]],
        ],
        color="blue",
        weight=2,
        opacity=0.9,
    ).add_to(m)

# 7. 저장
m.save("rerouted_paths_kakao_buffered_progress.html")
print("✅ 저장 완료: rerouted_paths_kakao_buffered_progress.html")
