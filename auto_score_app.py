import streamlit as st
import requests

# ==========================================
# 1. API 參數設定區 (已更換為您的 API-Sports 原廠金鑰)
# ==========================================
API_KEY = "92d87d7767e403abc4ca3d8adbcca6fc"

# ==========================================
# 2. 核心功能 (已修正為原廠專用網址與標頭)
# ==========================================
@st.cache_data(ttl=60)
def fetch_scores(season, date_str=None):
    url = "https://v3.football.api-sports.io/fixtures"
    querystring = {"league": "1", "season": season}
    if date_str:
        querystring["date"] = date_str
    
    # 這裡從 X-RapidAPI-Key 改成了原廠的 x-apisports-key
    headers = {
        "x-apisports-key": API_KEY
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get("errors"):
                return {"error": f"原廠回應錯誤：{res_json['errors']}"}
            return {"data": res_json.get("response", [])}
        elif response.status_code == 429:
            return {"error": "API 每日免費額度已用盡，請明天再試！"}
        else:
            return {"error": f"伺服器錯誤代碼：{response.status_code}"}
    except Exception as e:
        return {"error": f"系統連線異常：{e}"}

# ==========================================
# 3. 網頁介面
# ==========================================
st.set_page_config(page_title="世足賽即時比分", layout="centered")

st.title("🏆 世足賽即時比分看板 (單獨測試版)")

mode = st.radio("模式切換：", ["測試 (2022決賽)", "正式 (2026賽季)"], horizontal=True)

if mode == "測試 (2022決賽)":
    result = fetch_scores("2022", "2022-12-18")
else:
    result = fetch_scores("2026")

if "error" in result:
    st.error(f"❌ {result['error']}")
elif not result.get("data"):
    st.info("⚽ 該日或賽季目前無比賽資料。")
else:
    matches = result["data"]
    st.success(f"✅ 成功抓取 {len(matches)} 場資料！")
    
    for match in matches:
        home = match.get("teams", {}).get("home", {}).get("name", "未知名稱")
        away = match.get("teams", {}).get("away", {}).get("name", "未知名稱")
        h_score = match.get("goals", {}).get("home", 0)
        a_score = match.get("goals", {}).get("away", 0)
        status = match.get("fixture", {}).get("status", {}).get("short", "未知狀態")
        
        st.markdown("---")
        st.markdown(f"### 🏟️ {home} 🆚 {away}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label=home, value=h_score)
        col2.metric(label="賽事狀態", value=status)
        col3.metric(label=away, value=a_score)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 手動強制刷新", use_container_width=True):
    st.cache_data.clear()
    st.rerun()
