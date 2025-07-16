import streamlit as st
import pandas as pd

# ✅ CSV 파일 경로 (로컬 실행 시 수정)
FILE_PATH = "202505_202505_연령별인구현황_월간.csv"

# ✅ 데이터 불러오기 (EUC-KR)
df = pd.read_csv(FILE_PATH, encoding="euc-kr")

# ✅ 숫자형으로 변환 (쉼표 제거)
df = df.apply(lambda x: x.str.replace(",", "") if x.dtype == "object" else x)
df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")

# ✅ 필요한 컬럼 추출 및 컬럼명 전처리
total_pop_col = "2025년05월_계_총인구수"
age_cols = [col for col in df.columns if col.startswith("2025년05월_계_") and "총인구수" not in col and "연령구간" not in col]

# 연령 숫자만 추출 (예: '2025년05월_계_20세' → '20')
new_age_cols = {col: col.split("_")[-1].replace("세", "").replace("이상", "") for col in age_cols}
df = df.rename(columns=new_age_cols)

# ✅ 상위 5개 행정구역 추출 (총인구수 기준)
df_top5 = df.nlargest(5, total_pop_col)

# ✅ Streamlit 앱 시작
st.title("2025년 5월 기준 연령별 인구 현황 (상위 5개 행정구역)")
st.caption("출처: 행정안전부 주민등록 인구통계")

# ✅ 원본 데이터 표시
st.subheader("원본 데이터")
st.dataframe(df_top5)

# ✅ 연령별 인구 그래프 (상위 5개 행정구역)
st.subheader("연령별 인구 추이")
age_only_cols = list(new_age_cols.values())

# 연령순으로 정렬
age_only_cols = sorted([c for c in age_only_cols if c.isdigit()], key=int)

# 행정구역별 그래프
for idx, row in df_top5.iterrows():
    st.write(f"### {row['행정구역']}")
    st.line_chart(row[age_only_cols].rename("인구").to_frame())

