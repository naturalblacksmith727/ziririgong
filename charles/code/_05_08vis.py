import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. CSV 로드 (출발/도착 위경도 포함)
df = pd.read_csv("jeju_with_coords_kakao.csv", encoding='utf-8-sig')
df = df.dropna(subset=['출발_lat', '출발_lon', '도착_lat', '도착_lon'])

# 2. 격자 기준 정의 (제주도 범위 + 격자 크기 설정)
lat_min, lat_max = 33.1, 33.6
lon_min, lon_max = 126.1, 126.95
grid_size = 0.002  # 약 200m 단위 격자

n_rows = int((lat_max - lat_min) / grid_size)
n_cols = int((lon_max - lon_min) / grid_size)
heatmap = np.zeros((n_rows, n_cols))

# 3. 위경도 → 그리드 좌표 변환 함수


def latlon_to_grid(lat, lon):
    row = int((lat - lat_min) / grid_size)
    col = int((lon - lon_min) / grid_size)
    if 0 <= row < n_rows and 0 <= col < n_cols:
        return row, col
    return None, None

# 4. 경로 따라 선형 누적 (출발 → 도착)


def draw_line_on_heatmap(start, end):
    points = 100  # 중간 지점 수
    lats = np.linspace(start[0], end[0], points)
    lons = np.linspace(start[1], end[1], points)
    for lat, lon in zip(lats, lons):
        r, c = latlon_to_grid(lat, lon)
        if r is not None and c is not None:
            heatmap[r, c] += 1


# 5. 출발/도착지점에 가중치 추가
k = 5  # 출발/도착은 경로보다 k배 중요하다고 가정
for _, row in df.iterrows():
    start = (row['출발_lat'], row['출발_lon'])
    end = (row['도착_lat'], row['도착_lon'])

    draw_line_on_heatmap(start, end)

    for point in [start, end]:
        r, c = latlon_to_grid(*point)
        if r is not None and c is not None:
            heatmap[r, c] += (k - 1)

# 6. 로그 스케일로 시각화
plt.figure(figsize=(10, 8))
plt.imshow(np.log1p(heatmap), cmap='rainbow', origin='lower')
plt.title("jeju heatmap (grid = 200m)")
plt.xlabel("Longitude Grid")
plt.ylabel("Latitude Grid")
plt.colorbar(label="log(Intensity + 1)")
plt.tight_layout()
plt.show()
