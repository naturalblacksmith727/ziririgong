# import lxml
# import time
# import math
import requests
from bs4 import BeautifulSoup
import pandas
import pprint as pp

# #인코딩 됐을때
# service_key = '9VH8Dl7BNDE2r7qIa2XqmhsYk06C%2FeP%2BPppeVKS3lbCMbUMdL9pNWxQN3%2FpNKaTnvzf78DW%2FYmXEIn5V1YVcGg%3D%3D'

# #인코딩 안됐을때
# # service_key = rq.parse.quote(service_key, encoding='utf-8')

# # 인증키 포함 주소
# url = 'http://apis.data.go.kr/B552584/EvCharger/getChargerStatus'
# params = {'serviceKey': service_key,
#           'returnType': 'csv',
#           'pageNo': '1',
#           'numOfRows': '10',
#           'period': '5',
#           'zcode': '11'}

# response = requests.get(url, params=params)

# query = f"?ServiceKey={service_key}&returnType={returnType}&startDate={startdate}&endDate={enddate}"

# res = re.get(url + query)
# res.status_code
# dict_data = xtd.parse(res.text)
# pp.pprint(dict_data)


# import requests
# import urllib.parse

# service_key = 'yFqQ2sFmBBqWL89z46gTWtfoYGz%2FRUJahEHMHDPnBdq4Bg0gnpViM9SDHXfzOBUNWJttFBWZKzt3N%2Bc19phBqg%3D%3D'
# encoded_key = urllib.parse.quote(service_key, safe='')  # safe=''로 완전 인코딩

# url = "http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"
# params = {
#     'serviceKey': encoded_key,
#     'numOfRows': 10,
#     'pageNo': 1,
#     'dataType': 'JSON'
# }

# response = requests.get(url, params=params)

# print("응답 상태 코드:", response.status_code)
# print("응답 본문 (일부):", response.text[:500])  # 너무 길지 않게 출력

# # JSON 파싱 시도
# try:
#     data = response.json()
#     print("JSON 파싱 성공!")
# except Exception as e:
#     print("JSON 파싱 실패:", e)


# # 인증키 (발급받은 인증키를 여기에 입력하세요. 반드시 URL 인코딩되어야 합니다.)
# service_key = '9VH8Dl7BNDE2r7qIa2XqmhsYk06C%2FeP%2BPppeVKS3lbCMbUMdL9pNWxQN3%2FpNKaTnvzf78DW%2FYmXEIn5V1YVcGg%3D%3D'
# encoded_key = urllib.parse.quote(service_key)

# # 요청 URL 구성
# url = f"http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"
# params = {
#     'serviceKey': encoded_key,
#     'numOfRows': 10,
#     'pageNo': 1,
#     'dataType': 'JSON',  # 또는 'XML'
#     # 필요 시 아래 옵션도 추가 가능
#     # 'zcode': '11',  # 서울특별시
#     # 'zscode': '11680',  # 강남구
#     # 'kind': 'F0',  # 차량정비시설
#     # 'kindDetail': 'F002'  # 정비소
# }

# response = requests.get(url, params=params)
# if response.status_code == 200:
#     data = response.json()
#     items = data.get('items', {}).get('item', [])
#     for item in items:
#         print(f"충전소명: {item.get('statNm')}")
#         print(f"주소: {item.get('addr')} {item.get('addrDetail', '')}")
#         print(f"충전기ID: {item.get('chgerId')}")
#         print(f"충전상태: {item.get('stat')}")
#         print("-" * 40)
# else:
#     print("API 요청 실패:", response.status_code)


# # ------------------------------------------------------------
# response.content
# print(response.content)


# XML 생성하기

# req = requests.get(url)
# req.content

# soup = BeautifulSoup(req.content, "lxml")  # XML 생성

# # 데이터 가공
# # xml 형태를 pandas dataframe으로 만들기
# years = soup.find_all('acc_year')         # 접수년월
# sgg_cds = soup.find_all('sgg_cd')           # 자치구코드
# sgg_nms = soup.find_all('sgg_nm')           # 자치구명
# bjdong_cds = soup.find_all('bjdong_cd')        # 법정동코드
# bjdong_nms = soup.find_all('bjdong_nm')        # 법정동명
# land_gbns = soup.find_all('land_gbn')         # 지번구분
# land_gbn_nms = soup.find_all('land_gbn_nm')      # 지번구분명
# land_gbn_nms = soup.find_all('land_gbn_nm')      # 지번구분명
# bonbeons = soup.find_all('bonbeon')          # 본번
# bubeons = soup.find_all('bubeon')           # 부번
# bldg_nms = soup.find_all('bldg_nm')          # 건물명
# deal_ymds = soup.find_all('deal_ymd')         # 계약일
# obj_amts = soup.find_all('obj_amt')          # 물건금액(만원)
# bldg_areas = soup.find_all('bldg_area')        # 건물면적(㎡)
# tot_areas = soup.find_all('tot_area')         # 토지면적(㎡)
# floors = soup.find_all('floor')            # 층
# right_gbns = soup.find_all('right_gbn')        # 권리구분
# cntl_ymds = soup.find_all('cntl_ymd')         # 취소일
# build_years = soup.find_all('build_years')      # 건축년도
# house_types = soup.find_all('house_type')       # 건물용도
# req_gbn = soup.find_all('req_gbn')          # 신고구분
# rdealer_lawdnms = soup.find_all('rdealer_lawdnm')   # 신고한 개업공인중개사 시군구명

# # 반복문 활용
# year_list = []
# sgg_cd_list = []
# bldg_nm_list = []
# obj_amt_list = []
# house_type_list = []
# rdealer_lawdnm_list = []

# for year, sgg_cd, bldg_nm, obj_amt, house_type, rdealer_lawdnm in zip(years, sgg_cds, bldg_nms, obj_amts, house_types, rdealer_lawdnms):
#   year_list.append(year.get_text())
#   sgg_cd_list.append(sgg_cd.get_text())
#   bldg_nm_list.append(bldg_nm.get_text())
#   obj_amt_list.append(obj_amt.get_text())
#   house_type_list.append(house_type.get_text())
#   rdealer_lawdnm_list.append(rdealer_lawdnm.get_text())

# df = pd.DataFrame({
#     "acc_year": year_list,
#     "sgg_cd": sgg_cd_list,
#     "bldg_nm": bldg_nm_list,
#     "obj_amt": obj_amt_list,
#     "house_type": house_type_list,
#     "rdealer_lawdnm": rdealer_lawdnm_list
# })


import requests
import xml.etree.ElementTree as ET
import csv


# url = 'http://apis.data.go.kr/B552584/EvCharger/getChargerInfo'
# params = {'serviceKey': 'yFqQ2sFmBBqWL89z46gTWtfoYGz/RUJahEHMHDPnBdq4Bg0gnpViM9SDHXfzOBUNWJttFBWZKzt3N+c19phBqg==',
#           'pageNo': '1', 'numOfRows': '10', 'period': '5', 'zcode': '11'}

# response = requests.get(url, params=params)
# print(response.content)

# response.encoding = 'utf-8'  # 응답 인코딩 설정 (중요!)

# # XML 파싱
# root = ET.fromstring(response.text)
# items = root.findall(".//item")

# # CSV 파일로 저장
# with open("충전소_정보.csv", mode="w", newline="", encoding="utf-8-sig") as file:
#     writer = csv.writer(file)

#     # CSV 헤더 작성
#     writer.writerow([
#         "충전소명", "주소", "상세주소", "충전기ID", "충전방식", "충전상태", "설치년도"
#     ])

#     for item in items:
#         statNm = item.findtext("statNm", "")
#         addr = item.findtext("addr", "")
#         addrDetail = item.findtext("addrDetail", "")
#         chgerId = item.findtext("chgerId", "")
#         method = item.findtext("method", "")
#         stat = item.findtext("stat", "")
#         year = item.findtext("year", "")

#         # 상태 코드 매핑
#         status_map = {
#             "1": "통신이상",
#             "2": "사용가능",
#             "3": "충전중",
#             "4": "운영중지",
#             "5": "점검중",
#             "9": "상태미확인"
#         }
#         stat_desc = status_map.get(stat, "알 수 없음")

#         # 한 줄 작성
#         writer.writerow(
#             [statNm, addr, addrDetail, chgerId, method, stat_desc, year])

# print("✅ '충전소_정보.csv' 파일로 저장 완료!")

from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl
import certifi


service_key = "yFqQ2sFmBBqWL89z46gTWtfoYGz/RUJahEHMHDPnBdq4Bg0gnpViM9SDHXfzOBUNWJttFBWZKzt3N+c19phBqg=="

# 설정값
base_url = "http://apis.data.go.kr/B552584/EvCharger/getChargerStatus"

# # ssl 에러 확인용
# class TLSAdapter(HTTPAdapter):
#     def init_poolmanager(self, *args, **kwargs):
#         kwargs['ssl_version'] = ssl.PROTOCOL_TLSv1_2
#         kwargs['cert_reqs'] = ssl.CERT_REQUIRED
#         kwargs['ca_certs'] = certifi.where()
#         return super().init_poolmanager(*args, **kwargs)


# session = requests.Session()
# session.mount('https://', TLSAdapter())

# url = base_url  # 실제 URL로 바꿔주세요

# response = session.get(url)
# print(response.text)

params_base = {
    "serviceKey": service_key,
    "dataType": "XML",
    "numOfRows": 500,  # 최대 9999
    "pageNo": 1
}

# 먼저 1페이지 호출하여 전체 건수 확인
response = requests.get(base_url, params=params_base, verify=certifi.where())
response.encoding = 'utf-8'
root = ET.fromstring(response.text)
total_count = int(root.findtext(".//totalCount", default="0"))
print(f"🔍 전체 충전소 수: {total_count}건")

# 페이지 수 계산
num_per_page = params_base["numOfRows"]
total_pages = (total_count + num_per_page - 1) // num_per_page

# CSV 파일 열기
with open("충전소_전체정보2.csv", mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow([
        "충전소명", "주소", "상세주소", "충전기ID", "충전방식", "충전상태", "설치년도"
    ])

    # 페이지 순회
    for page in range(1, total_pages + 1):
        params_base["pageNo"] = page
        response = requests.get(base_url, params=params_base)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.text)
        items = root.findall(".//item")

        for item in items:
            statNm = item.findtext("statNm", "")
            addr = item.findtext("addr", "")
            addrDetail = item.findtext("addrDetail", "")
            chgerId = item.findtext("chgerId", "")
            method = item.findtext("method", "")
            stat = item.findtext("stat", "")
            year = item.findtext("year", "")

            status_map = {
                "1": "통신이상",
                "2": "사용가능",
                "3": "충전중",
                "4": "운영중지",
                "5": "점검중",
                "9": "상태미확인"
            }
            stat_desc = status_map.get(stat, "알 수 없음")

            writer.writerow([statNm, addr, addrDetail,
                            chgerId, method, stat_desc, year])

        print(f"📄 {page} / {total_pages} 페이지 완료")

print("✅ 전체 충전소 정보가 '충전소_전체정보.csv'에 저장되었습니다!")


# --------------------------------------------------------------------------------------------------------
# service_key = "yFqQ2sFmBBqWL89z46gTWtfoYGz/RUJahEHMHDPnBdq4Bg0gnpViM9SDHXfzOBUNWJttFBWZKzt3N+c19phBqg=="

# # 설정값
# base_url = "http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"
# params_base = {
#     "serviceKey": service_key,
#     "dataType": "XML",
#     "numOfRows": 300,  # 최대 9999
#     "pageNo": 1
# }

# # 먼저 1페이지 호출하여 전체 건수 확인
# response = requests.get(base_url, params=params_base)
# response.encoding = 'utf-8'
# root = ET.fromstring(response.text)
# total_count = int(root.findtext(".//totalCount", default="0"))
# print(f"🔍 전체 충전소 수: {total_count}건")

# # 페이지 수 계산
# num_per_page = params_base["numOfRows"]
# total_pages = (total_count + num_per_page - 1) // num_per_page

# # CSV 파일 열기
# with open("충전소_전체정보.csv", mode="w", newline="", encoding="utf-8-sig") as file:
#     writer = csv.writer(file)
#     writer.writerow([
#         "충전소명", "주소", "상세주소", "충전기ID", "충전방식", "충전상태", "설치년도"
#     ])

#     # 페이지 순회
#     for page in range(1, total_pages + 1):
#         params_base["pageNo"] = page
#         response = requests.get(base_url, params=params_base)
#         response.encoding = 'utf-8'
#         root = ET.fromstring(response.text)
#         items = root.findall(".//item")

#         for item in items:
#             statNm = item.findtext("statNm", "")
#             addr = item.findtext("addr", "")
#             addrDetail = item.findtext("addrDetail", "")
#             chgerId = item.findtext("chgerId", "")
#             method = item.findtext("method", "")
#             stat = item.findtext("stat", "")
#             year = item.findtext("year", "")

#             status_map = {
#                 "1": "통신이상",
#                 "2": "사용가능",
#                 "3": "충전중",
#                 "4": "운영중지",
#                 "5": "점검중",
#                 "9": "상태미확인"
#             }
#             stat_desc = status_map.get(stat, "알 수 없음")

#             writer.writerow([statNm, addr, addrDetail,
#                             chgerId, method, stat_desc, year])

#         print(f"📄 {page} / {total_pages} 페이지 완료")

# print("✅ 전체 충전소 정보가 '충전소_전체정보.csv'에 저장되었습니다!")
