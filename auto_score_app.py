import streamlit as st
import requests
from datetime import datetime

# ==========================================
# 1. API 設定區
# ==========================================
API_TOKEN = "d5921a999fd5418aa3c5026db3889cf2"

# ==========================================
# 2. 核心功能 (Football-Data.org 專用)
# ==========================================
@st.cache_data(ttl=60)
def fetch_scores(season="2026"):
    url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": API_TOKEN}
    params = {"season": season}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return {"data": response.json().get("matches", [])}
        elif response.status_code == 429:
            return {"error": "已達到每分鐘請求次數限制，請稍候再刷新。"}
        elif response.status_code == 403:
            msg = response.json().get("message", "權限不足，可能無法存取歷史賽事。")
            return {"error": f"原廠權限限制 (403)：{msg}"}
        else:
            return {"error": f"國際伺服器回應錯誤 (代碼 {response.status_code})"}
    except Exception as e:
        return {"error": f"系統連線異常：{e}"}

# ==========================================
# 3. 網頁介面
# ==========================================
st.set_page_config(page_title="世足賽即時比分", layout="centered")

st.title("🏆 世足賽即時比分看板 (單獨測試版)")

mode = st.radio("模式切換：", ["測試 (2022決賽)", "正式 (今日賽況)"], horizontal=True)

if st.button("🔄 手動強制刷新", use_container_width=True):
    st.cache_data.clear()

display_matches = []
is_error = False

# 邏輯區分：測試模式完全離線不連網
if mode == "測試 (2022決賽)":
    st.success("✅ 成功載入歷史測試資料！ (內建離線模式，不消耗 API 額度)")
    display_matches = [{
        "homeTeam": {"name": "Argentina"},
        "awayTeam": {"name": "France"},
        "score": {"fullTime": {"home": 3, "away": 3}},
        "status": "FINISHED"
    }]
else:
    result = fetch_scores(season="2026")
    if "error" in result:
        st.error(f"❌ {result['error']}")
        is_error = True
    else:
        all_matches = result.get("data", [])
        today_str = datetime.now().strftime("%Y-%m-%d")
        display_matches = [m for m in all_matches if m.get("utcDate", "").startswith(today_str)]

        if not display_matches:
            st.info(f"⚽ 今日 ({datetime.now().strftime('%Y-%m-%d')}) 暫無進行中的世界盃賽事。\n(提示：2026世界盃首場分組賽將於台北時間 6/12 03:00 正式開踢！)")
            is_error = True
        else:
            st.success(f"✅ 成功抓取 {len(display_matches)} 場資料！")

if not is_error and display_matches:
    status_map = {
        "FINISHED": "比賽結束", "IN_PLAY": "進行中", "PAUSED": "中場休息",
        "TIMED": "未開始", "SCHEDULED": "已排程", "POSTPONED": "延期"
    }
    
    for match in display_matches:
        home = match.get("homeTeam", {}).get("name", "未知名稱")
        away = match.get("awayTeam", {}).get("name", "未知名稱")
        
        score_data = match.get("score", {}).get("fullTime", {})
        h_score = score_data.get("home")
        a_score = score_data.get("away")
        h_score = 0 if h_score is None else h_score
        a_score = 0 if a_score is None else a_score
        
        status_raw = match.get("status", "UNKNOWN")
        status_text = status_map.get(status_raw, status_raw)
        
        st.markdown("---")
        st.markdown(f"### 🏟️ {home} 🆚 {away}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label=home, value=h_score)
        col2.metric(label="賽事狀態", value=status_text)
        col3.metric(label=away, value=a_score)
