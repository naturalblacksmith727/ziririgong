import pandas as pd
import folium

# 1. 데이터 불러오기
df_all = pd.read_csv("db\excel\최종사용 데이터\jeju_with_coords_kakao.csv")
df_reroute = pd.read_csv("db\excel\최종사용 데이터\hallasan_rerouted_paths.csv")
df_chargers = pd.read_csv("db\excel\최종사용 데이터\제주도_충전소_with_coords.csv")

# 2. 한라산 통과 경로 제거
filtered_df = df_all.merge(
    df_reroute[['출발_lat', '출발_lon', '도착_lat', '도착_lon']],
    how='left',
    on=['출발_lat', '출발_lon', '도착_lat', '도착_lon'],
    indicator=True
)
filtered_df = filtered_df[filtered_df['_merge'] == 'left_only'].drop(columns=[
                                                                     '_merge'])

# 3. 회피 경로 추가 병합
combined_df = pd.concat([filtered_df, df_reroute], ignore_index=True)

# 4. 충전소 NaN 좌표 제거
df_chargers = df_chargers.dropna(subset=['lat', 'lon'])

# 5. 지도 생성
m = folium.Map(location=[33.38, 126.55], zoom_start=11)

# 6. 경로 표시 (빨간 선, 우회 포함)
for _, row in combined_df.iterrows():
    if '우회_lat' in row and not pd.isna(row['우회_lat']):
        points = [
            [row['출발_lat'], row['출발_lon']],
            [row['우회_lat'], row['우회_lon']],
            [row['도착_lat'], row['도착_lon']]
        ]
    else:
        points = [
            [row['출발_lat'], row['출발_lon']],
            [row['도착_lat'], row['도착_lon']]
        ]
    folium.PolyLine(points, color='red', weight=2).add_to(m)

# 7. 충전소 표시 (파란 원)
for _, row in df_chargers.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=4,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.8
    ).add_to(m)

# 8. 저장
combined_df.to_csv("jeju_paths_with_reroute_and_chargers.csv", index=False)
m.save("jeju_paths_with_reroute_and_chargers.html")
