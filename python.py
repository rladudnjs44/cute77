import streamlit as st
import pandas as pd

# ✅ 페이지 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# ✅ CSV 파일 불러오기 (EUC-KR 인코딩)
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding="EUC-KR")

st.subheader("원본 데이터")
st.dataframe(df)

# ✅ 연령별 컬럼 이름 전처리
age_cols = [col for col in df.columns if col.startswith("2025년05월_계_")]
df_renamed = df.rename(columns={col: col.replace("2025년05월_계_", "") for col in age_cols})

# ✅ 필요한 컬럼만 선택
cols_to_use = ["행정구역", "총인구수"] + [col.replace("2025년05월_계_", "") for col in age_cols]
df_filtered = df_renamed[cols_to_use]

# ✅ 총인구수 기준 상위 5개 행정구역 추출
top5 = df_filtered.sort_values("총인구수", ascending=False).head(5)

st.subheader("총인구수 기준 상위 5개 행정구역")
st.dataframe(top5)

# ✅ 연령별 인구 선 그래프 그리기
st.subheader("상위 5개 행정구역 연령별 인구 선 그래프")

# 그래프용 데이터 변환
age_only_cols = [col for col in top5.columns if col not in ["행정구역", "총인구수"]]
top5_chart = top5.set_index("행정구역")[age_only_cols].T  # 연령을 세로축으로 하기 위해 전치

st.line_chart(top5_chart)

