from tqdm import tqdm
import pandas as pd
import json
import folium
from shapely.geometry import shape, Point, LineString
from shapely.ops import unary_union
from shapely.prepared import prep

# 파일 경로 (본인 경로에 맞게 수정)
csv_path = "db/hallasan_through_paths.csv"
geojson_path = "db/qgis/mt.hanlla_and_around.geojson"


# 1. GeoJSON 로드 및 병합
with open(geojson_path, "r", encoding="utf-8") as f:
    geo = json.load(f)
geometries = [shape(feat["geometry"]) for feat in geo["features"]]
hallasan_union = unary_union(geometries)
prepared_hallasan = prep(hallasan_union)

# 2. 통과 경로 불러오기
df_through = pd.read_csv(csv_path)

# 3. 버퍼 후보 생성 (10개)
buffer_start = 0.01
buffer_step = 0.005
num_candidates = 10

buffer_coords_list = []
for i in range(num_candidates):
    b = hallasan_union.buffer(buffer_start + i * buffer_step)
    coords = list(b.exterior.coords)
    buffer_coords_list.append(coords[::max(1, len(coords)//10)])

# 4. 우회 경로 계산
rerouted_records = []
print("🚧 회피 경로 계산 중...")
for _, row in tqdm(df_through.iterrows(), total=len(df_through)):
    sp = Point(row["출발_lon"], row["출발_lat"])
    ep = Point(row["도착_lon"], row["도착_lat"])
    reroute_found = False

    for coords in buffer_coords_list:
        for lat, lon in coords:
            mid = Point(lon, lat)
            l1 = LineString([sp, mid])
            l2 = LineString([mid, ep])
            if not prepared_hallasan.intersects(l1) and not prepared_hallasan.intersects(l2):
                rerouted_records.append({
                    "출발_lat": sp.y, "출발_lon": sp.x,
                    "우회_lat": mid.y, "우회_lon": mid.x,
                    "도착_lat": ep.y, "도착_lon": ep.x
                })
                reroute_found = True
                break
        if reroute_found:
            break

# 5. 저장
df_rerouted = pd.DataFrame(rerouted_records)
df_rerouted.to_csv("hallasan_rerouted_paths_step2.csv", index=False)
print("✅ 저장 완료: hallasan_rerouted_paths_step2.csv")

# 6. 시각화 (head 5개만)
m = folium.Map(location=[33.38, 126.55], zoom_start=11)
folium.GeoJson(hallasan_union).add_to(m)

for _, row in df_rerouted.head(5).iterrows():
    folium.PolyLine(
        locations=[
            [row["출발_lat"], row["출발_lon"]],
            [row["우회_lat"], row["우회_lon"]],
            [row["도착_lat"], row["도착_lon"]]
        ],
        color="blue", weight=3, opacity=0.8
    ).add_to(m)

m.save("hallasan_reroute_preview_head5.html")
print("🗺 저장 완료: hallasan_reroute_preview_head5.html")
