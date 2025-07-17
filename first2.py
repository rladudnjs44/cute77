import streamlit as st
import pandas as pd

st.title("📊 주민등록 인구 및 세대 현황 (2023.01 ~ 2024.01)")

# ✅ CSV 파일 직접 불러오기
file_path = "202301_202506_주민등록인구및세대현황_월간.csv"
df = pd.read_csv(file_path, encoding="euc-kr")

# ✅ 기간 컬럼 자동 탐색
date_cols = [col for col in df.columns if "기준" in col or "기간" in col or "월" in col]
if date_cols:
    date_col = date_cols[0]
    # 문자열을 날짜로 변환 (YYYY-MM 형태 지원)
    df[date_col] = pd.to_datetime(df[date_col].astype(str).str[:7], errors="coerce")

    # ✅ 2023년 1월 ~ 2024년 1월 필터링
    mask = (df[date_col] >= "2023-01-01") & (df[date_col] <= "2024-01-31")
    df = df[mask]
    df = df.dropna(subset=[date_col])
else:
    st.error("❌ 기간 컬럼을 찾지 못했습니다.")
    st.stop()

# ✅ 필터링된 데이터 표시
st.subheader("✅ 필터링된 데이터 (2023.01 ~ 2024.01)")
st.dataframe(df)

# ✅ 숫자형 컬럼 자동 탐색 후 시각화
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

if len(numeric_cols) == 0:
    st.error("❌ 시각화할 수 있는 숫자형 컬럼이 없습니다.")
else:
    y_col = numeric_cols[0]  # 첫 번째 숫자형 컬럼 사용
    chart_data = df.set_index(date_col)[[y_col]]  # ★ 날짜를 인덱스로 지정
    st.subheader(f"📈 '{y_col}' 변화 추이 (2023.01 ~ 2024.01)")
    st.line_chart(chart_data)

