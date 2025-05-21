import folium
from folium.plugins import HeatMap
import pandas as pd

# 좌표 포함된 CSV 로드
df = pd.read_csv("jeju_with_coords_kakao.csv")

# 지도 중심: 제주도
jeju_map = folium.Map(location=[33.38, 126.55], zoom_start=11)

# 중심 좌표 히트맵 데이터 생성
heat_data = df[['중심_lat', '중심_lon']].dropna().values.tolist()

# 히트맵 추가
HeatMap(heat_data).add_to(jeju_map)

# HTML로 저장
jeju_map.save("jeju_heatmap.html")
