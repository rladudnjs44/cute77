import streamlit as st
import pandas as pd

# ✅ CSV 파일 경로 (로컬 실행 시 수정)
FILE_PATH = "202505_202505_연령별인구현황_월간.csv"

# ✅ 데이터 불러오기 (EUC-KR)
df = pd.read_csv(FILE_PATH, encoding="euc-kr")

# ✅ 쉼표 제거 후 숫자로 변환
df = df.apply(lambda x: x.str.replace(",", "") if x.dtype == "object" else x)
df = df.apply(pd.to_numeric, errors="ignore")  # 변환 가능한 건 숫자로 변환

# ✅ 총인구수 컬럼을 숫자로 변환 (핵심 수정)
total_pop_col = "2025년05월_계_총인구수"
df[total_pop_col] = pd.to_numeric(df[total_pop_col], errors="coerce")

# ✅ 연령 관련 컬럼만 추출
age_cols = [
    col for col in df.columns
    if col.startswith("2025년05월_계_") and "총인구수" not in col and "연령구간" not in col
]

# ✅ 연령 컬럼명 전처리 (중복 방지)
def clean_age_col(col):
    age = col.split("_")[-1]
    if "이상" in age:
        return age.replace("세 이상", "이상").replace("세", "이상")
    else:
        return age.replace("세", "")

new_age_cols = {col: clean_age_col(col) for col in age_cols}
df = df.rename(columns=new_age_cols)

# ✅ 상위 5개 행정구역 추출 (총인구수 기준)
df_top5 = df.nlargest(5, total_pop_col).copy()

# ✅ Streamlit UI 시작
st.title("2025년 5월 기준 연령별 인구 현황 (상위 5개 행정구역)")
st.caption("출처: 행정안전부 주민등록 인구통계")

# ✅ 원본 데이터 표시
st.subheader("원본 데이터")
st.dataframe(df_top5)

# ✅ 연령별 인구 추이 (선 그래프)
st.subheader("연령별 인구 추이")

# 연령 컬럼 정렬
age_only_cols = [new_age_cols[c] for c in age_cols]
age_numeric = [a for a in age_only_cols if a.isdigit()]
age_special = [a for a in age_only_cols if not a.isdigit()]
age_sorted = sorted(age_numeric, key=int) + age_special

# ✅ 행정구역별 그래프
for _, row in df_top5.iterrows():
    st.write(f"### {row['행정구역']}")
    chart_data = row[age_sorted].rename("인구").to_frame()
    st.line_chart(chart_data)
