import streamlit as st
from common import page_header, data, expiry_status, fmt_money, ROUTINE_STEPS
from datetime import date

st.set_page_config(page_title="뷰티로그", page_icon="🧴", layout="wide")
st.markdown("""
<style>
.stApp {background:linear-gradient(180deg,#fff9fc 0%,#fffdfd 45%,#fff 100%);}
div[data-testid="stMetric"]{background:#fff;padding:.8rem;border:1px solid #f4dce8;border-radius:14px;}
div.stButton>button{border-radius:10px;}
</style>
""", unsafe_allow_html=True)

# 실제 페이지 파일을 사용하고 기본 Streamlit 사이드바 페이지 목록은 숨깁니다.
home = st.Page("pages/1_홈.py", title="홈", icon="🏠", default=True)
products = st.Page("pages/2_화장품_보관함.py", title="화장품 보관함", icon="🧴")
expiry = st.Page("pages/3_유통기한_관리.py", title="유통기한 관리", icon="⏰")
routine = st.Page("pages/4_루틴_체크.py", title="루틴 체크", icon="✨")
spending = st.Page("pages/5_소비_분석.py", title="소비 분석", icon="💸")
wishlist = st.Page("pages/6_위시리스트.py", title="위시리스트", icon="💗")

st.markdown("""
<div style="display:flex;align-items:center;gap:.65rem;margin:.2rem 0 1rem">
  <span style="font-size:2rem">🌸</span>
  <span style="font-size:1.8rem;font-weight:800;color:#63384f">뷰티로그</span>
  <span style="color:#927487">나만의 뷰티 관리</span>
</div>
""", unsafe_allow_html=True)
nav = st.columns(6)
items = [
    ("🏠 홈", home), ("🧴 보관함", products), ("⏰ 유통기한", expiry),
    ("✨ 루틴 체크", routine), ("💸 소비 분석", spending), ("💗 위시리스트", wishlist)
]
for col, (label, page) in zip(nav, items):
    with col:
        st.page_link(page, label=label, use_container_width=True)
st.divider()

# 유통기한이 내일인 제품은 모든 페이지 상단에 경고로 표시합니다.
tomorrow_items = [
    p for p in data["products"]
    if expiry_status(p) == ("내일 만료", 1)
]
if tomorrow_items:
    names = ", ".join(p.get("name", "이름 없는 제품") for p in tomorrow_items)
    st.warning(f"⚠️ **유통기한 하루 전 알림:** 다음 제품의 유통기한이 내일 끝나요: {names}")

from common import opened_use_status
use_tomorrow = [
    p for p in data["products"]
    if opened_use_status(p) == ("내일 사용기한 종료", 1)
]
if use_tomorrow:
    names = ", ".join(p.get("name", "이름 없는 제품") for p in use_tomorrow)
    st.warning(f"⚠️ **개봉 후 사용기한 하루 전:** 다음 제품의 개봉 후 사용기한이 내일 끝나요: {names}")

pg = st.navigation([home, products, expiry, routine, spending, wishlist], position="hidden")
pg.run()
