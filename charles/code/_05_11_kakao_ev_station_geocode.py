import pandas as pd
import requests
import time

KAKAO_API_KEY = 'aec31e8b4ee8a72e217e758078d058a5'
HEADERS = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

# 파일 로드
df = pd.read_csv("db/excel/제주도_충전소.csv")
df['lat'], df['lon'] = None, None


# 중복 주소 캐싱
coord_cache = {}


def kakao_geocode(address):
    if pd.isna(address):
        return None, None
    if address in coord_cache:
        return coord_cache[address]
    try:
        url = "https://dapi.kakao.com/v2/local/search/address.json"
        params = {"query": address}
        response = requests.get(url, headers=HEADERS, params=params, timeout=5)
        data = response.json().get("documents", [])
        if data:
            lat, lon = float(data[0]['y']), float(data[0]['x'])
            coord_cache[address] = (lat, lon)
            return lat, lon
    except:
        pass
    coord_cache[address] = (None, None)
    return None, None


# 진행률 추적
start = time.time()
total = len(df)

for i, row in df.iterrows():
    lat, lon = kakao_geocode(row['주소'])
    df.at[i, 'lat'] = lat
    df.at[i, 'lon'] = lon

    # 진행률 출력
    if i % 5 == 0 or i == total - 1:
        percent = (i + 1) / total * 100
        elapsed = time.time() - start
        est_total = elapsed / (i + 1) * total
        eta = est_total - elapsed
        print(
            f"[{i+1}/{total}] {percent:.1f}% 완료 | ⏱ 경과: {elapsed:.1f}s | ⌛ ETA: {eta:.1f}s")

    # 너무 빠르면 rate limit 걸릴 수 있음
    time.sleep(0.4)  # 줄이되, 0.2 이하로는 권장 안 함

# 저장
save_path = r"C:\Users\charl\OneDrive\Desktop\기타\coding\coding_on_study\ziririgon\First_project\db\excel제주도_충전소_with_coords.csv"
df.to_csv(save_path, index=False, encoding='utf-8-sig')
print(f"✅ 저장 완료: {save_path}")
