import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# CSV 파일 로드
df = pd.read_csv("jeju_final.csv")

# 지오코더 설정
geolocator = Nominatim(user_agent="jeju_geocoder")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# 위도/경도 추출 함수


def get_lat_lon(address):
    try:
        location = geocode(address)
        if location:
            return pd.Series([location.latitude, location.longitude])
    except:
        return pd.Series([None, None])
    return pd.Series([None, None])


# 출발/도착 위경도
df[['출발_lat', '출발_lon']] = df['출발 주소'].apply(get_lat_lon)
df[['도착_lat', '도착_lon']] = df['도착 주소'].apply(get_lat_lon)

# 중심 좌표
df['중심_lat'] = (df['출발_lat'] + df['도착_lat']) / 2
df['중심_lon'] = (df['출발_lon'] + df['도착_lon']) / 2

# 결과 저장
df.to_csv("jeju_with_coordinates.csv", index=False)
