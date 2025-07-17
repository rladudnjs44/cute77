import streamlit as st
import pandas as pd

st.title("📊 주민등록 인구 및 세대 현황 (2023.01 ~ 2024.01)")

# ✅ CSV 파일 경로 (같은 디렉토리에 있을 때)
file_path = "202301_202506_주민등록인구및세대현황_월간.csv"

# CSV 불러오기 (EUC-KR 인코딩)
df = pd.read_csv(file_path, encoding="euc-kr")

# ---- 기간 컬럼 자동 추정 ----
date_cols = [col for col in df.columns if "기준" in col or "기간" in col or "월" in col]
if date_cols:
    date_col = date_cols[0]
    # 문자열을 날짜형으로 변환 시도
    try:
        df[date_col] = pd.to_datetime(df[date_col])
    except:
        # 변환 실패 시, 앞 7자리(YYYY-MM)만 잘라서 변환
        df[date_col] = pd.to_datetime(df[date_col].astype(str).str[:7], errors="coerce")

    # ✅ 2023년 1월 ~ 2024년 1월까지만 필터링
    start_date = pd.Timestamp("2023-01-01")
    end_date = pd.Timestamp("2024-01-31")
    df = df[(df[date_col] >= start_date) & (df[date_col] <= end_date)]
else:
    st.warning("기간(월)을 나타내는 컬럼을 찾지 못했습니다. 전체 데이터를 사용합니다.")

# ✅ 필터링된 데이터 출력
st.subheader("✅ 필터링된 데이터 (2023.01 ~ 2024.01)")
st.dataframe(df)

# ✅ 시각화 (첫 번째 숫자형 컬럼 기준)
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

if len(numeric_cols) > 0:
    y_col = numeric_cols[0]
    if date_cols:
        chart_data = df.set_index(date_col)[y_col]
    else:
        chart_data = df[y_col]

    st.subheader(f"📈 '{y_col}' 변화 추이 (2023.01 ~ 2024.01)")
    st.line_chart(chart_data)
else:
    st.warning("시각화할 수 있는 숫자형 데이터가 없습니다.")
