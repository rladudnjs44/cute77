import streamlit as st
import pandas as pd

# 앱 제목
st.title("📊 주민등록 인구 및 세대 현황 (월간)")

# CSV 파일 불러오기 (EUC-KR 인코딩)
file_path = "202301_202506_주민등록인구및세대현황_월간.csv"
df = pd.read_csv(file_path, encoding="euc-kr")

# 원본 데이터 표시
st.subheader("✅ 원본 데이터")
st.dataframe(df)

# 숫자형 컬럼만 필터링
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

if len(numeric_cols) > 0:
    # 첫 번째 숫자형 컬럼을 y축으로 사용
    y_col = numeric_cols[0]

    # x축은 인덱스 또는 '기간'/'월' 등의 첫 번째 텍스트형 컬럼 추정
    possible_x_cols = df.select_dtypes(include=['object']).columns.tolist()
    if possible_x_cols:
        x_col = possible_x_cols[0]
        chart_data = df.set_index(x_col)[y_col]
    else:
        chart_data = df[y_col]

    st.subheader(f"📈 '{y_col}' 변화 추이")
    st.line_chart(chart_data)
else:
    st.warning("시각화할 수 있는 숫자형 데이터가 없습니다.")
