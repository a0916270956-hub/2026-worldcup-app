import streamlit as st
import requests
from datetime import datetime

# ==========================================
# 1. 設定區 (已綁定您的 API Key)
# ==========================================
RAPID_API_KEY = "5048786a54mshe1078420ed5662ap154c43jsndcfb158f929a" 
API_HOST = "api-football-v1.p.rapidapi.com"

# ==========================================
# 2. 核心功能：連網抓取數據
# ==========================================
@st.cache_data(ttl=60)
def fetch_scores(season, date_str=None):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    # 若提供日期則抓取該日賽事，若無則抓取該賽季即時比賽
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
            data = response.json()
            if data.get("errors"):
                return {"error_msg": str(data["errors"])}
            return {"data": data.get("response", [])}
        else:
            return {"error_msg": f"連線失敗，狀態碼：{response.status_code}"}
    except Exception as e:
        return {"error_msg": str(e)}

# ==========================================
# 3. 網頁介面
# ==========================================
st.set_page_config(page_title="2026世足自動比分", page_icon="🏆", layout="centered")

st.title("🏆 2026 世足賽自動比分看板")
st.markdown("系統自動同步國際比賽數據，無需手動更新。")

# 模式切換：測試(2022歷史) vs 正式(2026)
mode = st.radio("模式選擇：", ["測試模式 (2022決賽)", "正式模式 (2026賽季)"], horizontal=True)

if mode == "測試模式 (2022決賽)":
    result = fetch_scores(season="2022", date_str="2022-12-18")
else:
    result = fetch_scores(season="2026")

# 錯誤處理與顯示邏輯
if "error_msg" in result:
    st.error("❌ 連線錯誤，請檢查您的 API 權限：")
    st.write(result["error_msg"])
elif not result.get("data"):
    st.warning("⚽ 目前無賽事數據，請稍後再試。")
else:
    matches = result["data"]
    st.success(f"✅ 成功獲取 {len(matches)} 場賽事資訊！")
    
    for match in matches:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        h_score = match["goals"]["home"] or 0
        a_score = match["goals"]["away"] or 0
        status = match["fixture"]["status"]["short"]
        
        st.markdown("---")
        c1, c2, c3 = st.columns([3, 1, 3])
        with c1:
            st.subheader(home)
        with c2:
            st.markdown(f"<h2 style='text-align: center; color: red;'>{h_score} - {a_score}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>{status}</p>", unsafe_allow_html=True)
        with c3:
            st.subheader(away)

if st.button("🔄 強制刷新"):
    st.cache_data.clear()
    st.rerun()
