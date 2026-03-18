from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import requests
import streamlit as st

API_KEY = "여기에_KOBIS_API_KEY를_입력하세요"
KOBIS_DAILY_BOXOFFICE_URL = (
    "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)


def get_api_key() -> str:
    secret_key = st.secrets.get("KOBIS_API_KEY", "")
    if secret_key:
        return str(secret_key)
    return API_KEY


@st.cache_data(show_spinner=False, ttl=3600)
def fetch_daily_box_office(target_date: str) -> pd.DataFrame:
    api_key = get_api_key()
    response = requests.get(
        KOBIS_DAILY_BOXOFFICE_URL,
        params={"key": api_key, "targetDt": target_date},
        timeout=10,
    )
    response.raise_for_status()

    payload = response.json()
    box_office_result = payload.get("boxOfficeResult", {})
    daily_list = box_office_result.get("dailyBoxOfficeList", [])

    if not daily_list:
        return pd.DataFrame()

    df = pd.DataFrame(daily_list)

    numeric_columns = [
        "rank",
        "salesAmt",
        "salesShare",
        "salesInten",
        "salesChange",
        "salesAcc",
        "audiCnt",
        "audiInten",
        "audiChange",
        "audiAcc",
        "scrnCnt",
        "showCnt",
    ]
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def format_number(value: float | int) -> str:
    if pd.isna(value):
        return "-"
    return f"{int(value):,}"


st.set_page_config(
    page_title="영화 박스오피스 대시보드",
    page_icon="🎬",
    layout="wide",
)

st.title("영화 박스오피스 대시보드")
st.caption("영화진흥위원회(KOBIS) 일별 박스오피스 데이터를 조회합니다.")

if get_api_key() == "여기에_KOBIS_API_KEY를_입력하세요":
    st.warning(
        "`st.secrets`의 `KOBIS_API_KEY` 또는 `app.py`의 `API_KEY` 값에 "
        "본인의 KOBIS API 키를 입력하세요."
    )
    st.stop()

default_date = date.today() - timedelta(days=1)
selected_date = st.date_input(
    "조회 날짜를 선택하세요",
    value=default_date,
    max_value=default_date,
    help="KOBIS 일별 박스오피스는 일반적으로 전일 기준 데이터가 안정적입니다.",
)

target_date = selected_date.strftime("%Y%m%d")

try:
    df = fetch_daily_box_office(target_date)
except requests.HTTPError as exc:
    st.error(f"API 요청에 실패했습니다. 응답 상태 코드를 확인하세요: {exc}")
    st.stop()
except requests.RequestException as exc:
    st.error(f"네트워크 오류가 발생했습니다: {exc}")
    st.stop()
except ValueError:
    st.error("API 응답을 JSON으로 해석하지 못했습니다. API 키와 응답 형식을 확인하세요.")
    st.stop()

if df.empty:
    st.info("해당 날짜의 박스오피스 데이터가 없습니다.")
    st.stop()

top10_df = (
    df.sort_values("rank")
    .head(10)
    .loc[:, ["rank", "movieNm", "audiCnt", "audiAcc", "salesAmt", "openDt", "rankOldAndNew"]]
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("조회 날짜", selected_date.strftime("%Y-%m-%d"))
with col2:
    st.metric("1위 영화", str(top10_df.iloc[0]["movieNm"]))
with col3:
    st.metric("1위 관객 수", format_number(top10_df.iloc[0]["audiCnt"]))

chart_df = top10_df.set_index("movieNm")[["audiCnt"]]
st.subheader("1~10위 영화 관객 수")
st.bar_chart(chart_df)

display_df = top10_df.rename(
    columns={
        "rank": "순위",
        "movieNm": "영화명",
        "audiCnt": "당일 관객 수",
        "audiAcc": "누적 관객 수",
        "salesAmt": "매출액",
        "openDt": "개봉일",
        "rankOldAndNew": "신작 여부",
    }
)

st.subheader("상세 데이터")
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "순위": st.column_config.NumberColumn(format="%d"),
        "당일 관객 수": st.column_config.NumberColumn(format="%d명"),
        "누적 관객 수": st.column_config.NumberColumn(format="%d명"),
        "매출액": st.column_config.NumberColumn(format="%d원"),
        "개봉일": st.column_config.TextColumn(),
        "신작 여부": st.column_config.TextColumn(help="NEW 또는 OLD"),
    },
)
