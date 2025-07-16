import streamlit as st
import pandas as pd

# -----------------------------
# 1. 데이터 불러오기 및 전처리 함수
# -----------------------------
@st.cache_data
def load_data():
    # CSV 불러오기 (EUC-KR 인코딩)
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding="EUC-KR")

    # 열 이름 공백 제거
    df.columns = df.columns.str.strip()

    # 중복된 열 제거 (총인구수 같은 중복 방지)
    df = df.loc[:, ~df.columns.duplicated()]

    return df

df = load_data()

# -----------------------------
# 2. UI 제목
# -----------------------------
st.title("2025년 5월 기준 연령별 인구 현황")
st.write("### ✅ 원본 데이터")
st.dataframe(df)

# -----------------------------
# 3. 연령 컬럼 전처리
# -----------------------------
# "2025년05월_계_"로 시작하는 컬럼만 선택
age_cols = [col for col in df.columns if col.startswith("2025년05월_계_")]

# 열 이름을 연령 숫자로 변경 (예: "2025년05월_계_0세" → "0")
rename_dict = {
    col: col.replace("2025년05월_계_", "").replace("세", "").strip()
    for col in age_cols
}
df = df.rename(columns=rename_dict)

# -----------------------------
# 4. 분석용 데이터 준비
# -----------------------------
columns_to_use = ["총인구수"] + list(rename_dict.values())
df_analysis = df[["행정구역"] + columns_to_use]

# 총인구수 상위 5개 행정구역 추출
top5 = df_analysis.sort_values("총인구수", ascending=False).head(5)
top5 = top5.set_index("행정구역")

st.write("### ✅ 총인구수 기준 상위 5개 행정구역")
st.dataframe(top5)

# -----------------------------
# 5. 연령별 인구 현황 시각화 (Streamlit 기본 기능)
# -----------------------------
ages = [col for col in top5.columns if col != "총인구수"]
top5_age = top5[ages].T  # 전치하여 연령이 행, 행정구역이 열
top5_age.index = top5_age.index.astype(int)  # 연령을 숫자로 변환
top5_age = top5_age.sort_index()

st.write("### ✅ 연령별 인구 현황 (상위 5개 행정구역)")
st.line_chart(top5_age)
