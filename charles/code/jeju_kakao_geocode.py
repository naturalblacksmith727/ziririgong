import pandas as pd
import requests
import time

# 사용자 입력 필요: 여기에 본인의 카카오 REST API 키 입력
KAKAO_API_KEY = "aec31e8b4ee8a72e217e758078d058a5"
HEADERS = {
    "Authorization": f"KakaoAK {KAKAO_API_KEY}"
}

# 파일 경로
INPUT_PATH = "jeju_final.csv"
OUTPUT_PATH = "jeju_with_coords_kakao.csv"

# 데이터 로드
df = pd.read_csv(INPUT_PATH)

# 좌표 캐시
coord_cache = {}

# 카카오 API 요청 함수


def kakao_geocode(address):
    if pd.isna(address):
        return None, None
    if address in coord_cache:
        return coord_cache[address]

    try:
        url = "https://dapi.kakao.com/v2/local/search/address.json"
        params = {"query": address}
        response = requests.get(url, headers=HEADERS, params=params, timeout=5)

        if response.status_code != 200:
            print(f"❌ 응답 실패 [{response.status_code}] - {address}")
            coord_cache[address] = (None, None)
            return None, None

        data = response.json()
        docs = data.get("documents", [])
        if docs:
            lat = float(docs[0]["y"])
            lon = float(docs[0]["x"])
            coord_cache[address] = (lat, lon)
            return lat, lon
        else:
            print(f"⚠️ 좌표 없음: {address}")
    except Exception as e:
        print(f"❌ 오류 - {address}: {str(e)}")

    coord_cache[address] = (None, None)
    return None, None


# 좌표 리스트 초기화
출발_lat, 출발_lon, 도착_lat, 도착_lon = [], [], [], []

start = time.time()

for idx, row in df.iterrows():
    s_addr = row['출발 주소']
    d_addr = row['도착 주소']

    s_lat, s_lon = kakao_geocode(s_addr)
    d_lat, d_lon = kakao_geocode(d_addr)

    출발_lat.append(s_lat)
    출발_lon.append(s_lon)
    도착_lat.append(d_lat)
    도착_lon.append(d_lon)

    if idx % 10 == 0:
        print(f"[{idx}/{len(df)}] 완료 ⏱ {(time.time() - start):.1f}초 경과")

# 좌표 저장
df['출발_lat'] = pd.Series(출발_lat, dtype='float')
df['출발_lon'] = pd.Series(출발_lon, dtype='float')
df['도착_lat'] = pd.Series(도착_lat, dtype='float')
df['도착_lon'] = pd.Series(도착_lon, dtype='float')

# 열 순서 재배열
columns_keep = [
    '출발행정코드', '도착행정코드',
    '출발 주소', '도착 주소',
    '출발_lat', '출발_lon',
    '도착_lat', '도착_lon'
]
df = df[columns_keep]

# 파일 저장 (한글 호환을 위해 utf-8-sig 사용)
df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8-sig')
print(f"\n✅ 저장 완료: {OUTPUT_PATH}")
