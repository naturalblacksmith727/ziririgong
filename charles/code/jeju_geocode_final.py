import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# 파일 경로
INPUT_PATH = "jeju_final.csv"
OUTPUT_PATH = "jeju_with_coords_clean.csv"

# CSV 로드
df = pd.read_csv(INPUT_PATH)

# 지오코더 설정
geolocator = Nominatim(user_agent="jeju_mapper", timeout=10)
geocode = RateLimiter(
    geolocator.geocode,
    min_delay_seconds=1,
    max_retries=3,
    error_wait_seconds=5.0
)

# 좌표 캐시
coord_cache = {}

# 캐시 기반 좌표 추출 함수


def get_lat_lon_cached(address):
    if pd.isna(address):
        return (None, None)
    if address in coord_cache:
        return coord_cache[address]
    try:
        location = geocode(address)
        if location:
            coord_cache[address] = (
                float(location.latitude), float(location.longitude))
        else:
            coord_cache[address] = (None, None)
    except Exception as e:
        print(f"❌ 오류 발생 - 주소: {address} / 메시지: {str(e)}")
        coord_cache[address] = (None, None)
    return coord_cache[address]


# 위경도 수집
출발_lat, 출발_lon, 도착_lat, 도착_lon = [], [], [], []
total = len(df)
start_time = time.time()

for idx, row in df.iterrows():
    s_lat, s_lon = get_lat_lon_cached(row['출발 주소'])
    d_lat, d_lon = get_lat_lon_cached(row['도착 주소'])

    출발_lat.append(s_lat)
    출발_lon.append(s_lon)
    도착_lat.append(d_lat)
    도착_lon.append(d_lon)

    if idx % 10 == 0:
        elapsed = time.time() - start_time
        print(f"[{idx}/{total}] 처리 중... ⏱ {elapsed:.1f}s 경과")

# DataFrame에 추가
df['출발_lat'] = pd.Series(출발_lat, dtype='float')
df['출발_lon'] = pd.Series(출발_lon, dtype='float')
df['도착_lat'] = pd.Series(도착_lat, dtype='float')
df['도착_lon'] = pd.Series(도착_lon, dtype='float')

# 열 순서 지정 및 나머지 열 삭제
columns_keep = [
    '출발행정코드', '도착행정코드',
    '출발 주소', '도착 주소',
    '출발_lat', '출발_lon',
    '도착_lat', '도착_lon'
]
df = df[columns_keep]

# 저장
df.to_csv(OUTPUT_PATH, index=False)
print(f"\n✅ 저장 완료: {OUTPUT_PATH}")
