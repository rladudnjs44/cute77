import streamlit as st
import pandas as pd

# 앱 제목
st.title("📊 주민등록 인구 및 세대 현황 (월간)")

# 파일 업로드 UI
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (EUC-KR 인코딩)", type=["csv"])

if uploaded_file is not None:
    # CSV 읽기
    df = pd.read_csv(uploaded_file, encoding="euc-kr")

    # 원본 데이터 표시
    st.subheader("✅ 원본 데이터")
    st.dataframe(df)

    # 숫자형 컬럼만 필터링
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    if len(numeric_cols) > 0:
        # 첫 번째 숫자형 컬럼을 y축으로 사용
        y_col = numeric_cols[0]

        # x축은 첫 번째 문자열(object) 컬럼 사용 시도
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
else:
    st.info("왼쪽에서 CSV 파일을 업로드해주세요.")
