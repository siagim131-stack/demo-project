import json
from pathlib import Path
from datetime import date, datetime, timedelta
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "beautylog_data.json"
CATEGORIES = ["스킨케어", "선케어", "메이크업", "클렌징", "바디케어", "헤어케어", "향수", "기타"]
SKIN_TYPES = ["모든 피부", "건성", "지성", "복합성", "민감성"]
ROUTINE_STEPS = {
    "아침": ["세안", "토너", "에센스/세럼", "로션/크림", "선크림"],
    "저녁": ["클렌징", "토너", "에센스/세럼", "로션/크림", "립케어"],
}
DEFAULT_DATA = {"products": [], "routine_checks": {}, "expenses": [], "wishlist": []}

def load_data():
    if DATA_FILE.exists():
        try:
            loaded = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            for key, value in DEFAULT_DATA.items():
                loaded.setdefault(key, value.copy())
            return loaded
        except (OSError, json.JSONDecodeError):
            st.warning("저장 파일을 읽지 못해 새 데이터를 사용합니다.")
    return {key: value.copy() for key, value in DEFAULT_DATA.items()}

if "data" not in st.session_state:
    st.session_state.data = load_data()
data = st.session_state.data

def save_data():
    DATA_FILE.write_text(json.dumps(st.session_state.data, ensure_ascii=False, indent=2), encoding="utf-8")

def fmt_money(value):
    return f"{int(value):,}원"

def parse_date(value):
    try:
        return date.fromisoformat(value) if value else None
    except (ValueError, TypeError):
        return None

def expiry_status(product):
    expiry = parse_date(product.get("expiry_date", ""))
    if not expiry:
        return "날짜 미입력", None
    days = (expiry - date.today()).days
    if days < 0:
        return "기한 지남", days
    if days == 1:
        return "내일 만료", days
    if days <= 30:
        return "임박", days
    return "여유", days

def add_expense(name, amount, purchase_date, category):
    data["expenses"].append({
        "id": f"e{datetime.now().timestamp()}",
        "name": name, "amount": int(amount),
        "date": purchase_date.isoformat(), "category": category
    })

def page_header(title, subtitle):
    st.markdown(f"""
    <div style="padding:1rem 1.3rem;border-radius:18px;background:linear-gradient(120deg,#ffe3ef,#f4e8ff);margin-bottom:1rem">
      <h1 style="margin:0;color:#63384f">{title}</h1>
      <p style="margin:.35rem 0 0;color:#76566a">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def opened_use_status(product):
    """개봉 후 사용기한 날짜를 기준으로 상태를 반환합니다."""
    use_by = parse_date(product.get("use_by_date", ""))
    if not product.get("opened", False) or not use_by:
        return "미설정", None
    days = (use_by - date.today()).days
    if days < 0:
        return "사용기한 지남", days
    if days == 1:
        return "내일 사용기한 종료", days
    if days <= 30:
        return "사용기한 임박", days
    return "여유", days
