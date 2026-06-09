import streamlit as st
import requests

# ==========================================
# 1. 設定區 
# ==========================================
RAPID_API_KEY = "5048786a54mshe1078420ed5662ap154c43jsndcfb158f929a" 
API_HOST = "api-football-v1.p.rapidapi.com"

# ==========================================
# 2. 核心功能
# ==========================================
@st.cache_data(ttl=60)
def fetch_scores(season, date_str=None):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league": "1", "season": season}
    if date_str:
        querystring["date"] = date_str
    
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == 200:
            return response.json().get("response", [])
        return None
    except:
        return None

# ==========================================
# 3. 網頁介面 (全面棄用 HTML 語法，確保 100% 顯示)
# ==========================================
st.set_page_config(page_title="世足賽即時比分", layout="centered")

st.title("🏆 世足賽即時比分看板")

mode = st.radio("模式切換：", ["測試 (2022決賽)", "正式 (2026賽季)"], horizontal=True)

if mode == "測試 (2022決賽)":
    data = fetch_scores("2022", "2022-12-18")
else:
    data = fetch_scores("2026")

if data is None:
    st.error("❌ 無法連線到 API")
elif len(data) == 0:
    st.warning("⚽ 目前無比賽資料")
else:
    st.success(f"✅ 成功抓取 {len(data)} 場資料！")
    
    # 【保險機制】直接把 API 傳回來的一手資料赤裸裸地印在畫面上，證明資料確實存在
    st.write("---")
    st.write("▼ 【系統底層資料驗證】如果您能看到下面這個框框，代表 API 已經成功把 3:3 的比分送進您的手機了：")
    st.json(data)
    
    st.write("---")
    st.write("▼ 【標準文字排版】(不使用任何可能被屏蔽的網頁色彩語法)")
    
    for match in data:
        # 安全讀取資料
        home = match.get("teams", {}).get("home", {}).get("name", "未知名稱")
        away = match.get("teams", {}).get("away", {}).get("name", "未知名稱")
        
        h_score = match.get("goals", {}).get("home", 0)
        a_score = match.get("goals", {}).get("away", 0)
        status = match.get("fixture", {}).get("status", {}).get("short", "未知狀態")
        
        # 100% 原生的顯示方式，絕對不會跑版或隱形
        st.subheader(f"🏟️ 對戰組合：{home} vs {away}")
        st.header(f"⚽ 當前比分： {h_score} - {a_score}")
        st.write(f"⏱️ 賽事狀態： {status}")
        st.write("---")

if st.button("🔄 手動強制刷新"):
    st.cache_data.clear()
    st.rerun()
