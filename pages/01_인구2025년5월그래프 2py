import streamlit as st
import pandas as pd

# ✅ CSV 파일 경로
FILE_PATH = "202505_202505_연령별인구현황_월간.csv"

# ✅ 데이터 불러오기 (EUC-KR)
df = pd.read_csv(FILE_PATH, encoding="euc-kr")

# ✅ 쉼표 제거 후 숫자로 변환
df = df.apply(lambda x: x.str.replace(",", "") if x.dtype == "object" else x)
df = df.apply(pd.to_numeric, errors="ignore")

# ✅ 총인구수 숫자 변환
total_pop_col = "2025년05월_계_총인구수"
df[total_pop_col] = pd.to_numeric(df[total_pop_col], errors="coerce")

# ✅ 상위 5개 행정구역 추출
df_top5 = df.nlargest(5, total_pop_col).copy()

# ✅ 행정구역 → 위도/경도 매핑 (대표 좌표, 필요시 추가)
geo_mapping = {
    "서울특별시": [37.5665, 126.9780],
    "부산광역시": [35.1796, 129.0756],
    "인천광역시": [37.4563, 126.7052],
    "대구광역시": [35.8714, 128.6014],
    "대전광역시": [36.3504, 127.3845],
    "광주광역시": [35.1595, 126.8526],
    "울산광역시": [35.5384, 129.3114],
    "경기도": [37.4138, 127.5183],
    "경상남도": [35.2372, 128.6917],
    "경상북도": [36.4919, 128.8889],
    "충청북도": [36.6357, 127.4917],
    "충청남도": [36.5184, 126.8],
    "전라북도": [35.7175, 127.153],
    "전라남도": [34.8161, 126.463],
    "강원특별자치도": [37.8228, 128.1555],
    "제주특별자치도": [33.4996, 126.5312]
}

# ✅ 위도/경도 컬럼 추가
df_top5["위도"] = df_top5["행정구역"].map(lambda x: geo_mapping.get(x.split()[0], [0, 0])[0])
df_top5["경도"] = df_top5["행정구역"].map(lambda x: geo_mapping.get(x.split()[0], [0, 0])[1])

# ✅ Streamlit UI 시작
st.title("2025년 5월 기준 연령별 인구 현황 (상위 5개 행정구역)")
st.caption("출처: 행정안전부 주민등록 인구통계")

# ✅ 원본 데이터 표시
st.subheader("원본 데이터")
st.dataframe(df_top5[["행정구역", total_pop_col, "위도", "경도"]])

# ✅ 지도 시각화
st.subheader("상위 5개 행정구역 위치")
st.map(df_top5.rename(columns={"위도": "lat", "경도": "lon"}))
