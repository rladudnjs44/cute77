import streamlit as st
import pandas as pd

# -----------------------------
# 1. 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="EUC-KR")
    return df

df = load_data()

st.title("2025년 5월 기준 연령별 인구 현황")
st.write("### 원본 데이터")
st.dataframe(df)

# -----------------------------
# 2. 데이터 전처리
# -----------------------------
# 연령별 열 이름 전처리 (예: "2025년05월_계_0세" → "0세" → 숫자만)
age_cols = [col for col in df.columns if col.startswith("2025년05월_계_")]
rename_dict = {col: col.replace("2025년05월_계_", "").replace("세", "") for col in age_cols}
df = df.rename(columns=rename_dict)

# 분석에 필요한 컬럼만 선택 (총인구수 + 연령별)
columns_to_use = ["총인구수"] + list(rename_dict.values())
df_analysis = df[["행정구역"] + columns_to_use]

# -----------------------------
# 3. 총인구수 기준 상위 5개 행정구역 선택
# -----------------------------
top5 = df_analysis.nlargest(5, "총인구수").set_index("행정구역")

st.write("### 총인구수 기준 상위 5개 행정구역")
st.dataframe(top5)

# -----------------------------
# 4. 선 그래프 시각화 (Streamlit 기본 기능)
# -----------------------------
# 연령 열만 추출
ages = [col for col in top5.columns if col != "총인구수"]
top5_age = top5[ages].T  # 행: 연령, 열: 행정구역
top5_age.index = top5_age.index.astype(int)  # 연령을 숫자로 변환 후 정렬
top5_age = top5_age.sort_index()

st.write("### 연령별 인구 현황 (상위 5개 행정구역)")
st.line_chart(top5_age)
