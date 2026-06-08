import streamlit as st
import requests
from datetime import datetime

# ==========================================
# 1. 設定區 (已帶入您的專屬 API Key)
# ==========================================
RAPID_API_KEY = "5048786a54mshe1078420ed5662ap154c43jsndcfb158f929a" 
API_HOST = "api-football-v1.p.rapidapi.com"

# ==========================================
# 2. 核心功能：連網抓取數據 (改為歷史測試版)
# ==========================================
@st.cache_data(ttl=60)
def fetch_live_scores():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    # 【關鍵修改點】：賽季改為 2022，移除 live 參數，加入決賽日期 (2022-12-18)
    querystring = {"league": "1", "season": "2022", "date": "2022-12-18"}
    
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        
        if response.status_code == 200:
            return response.json().get("response", [])
        else:
            st.error(f"API 連線失敗，狀態碼：{response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        st.error(f"網路連線發生異常: {e}")
        return []

# ==========================================
# 3. 網頁介面與資料解析
# ==========================================
st.set_page_config(page_title="測試中: 世足比分排版", page_icon="📡")

st.title("📡 API 連線測試：2022 世足決賽")
st.markdown("此為測試版，用來確認您的 API 金鑰是否有效，以及排版是否正常。")

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.caption(f"🔄 最後更新時間：{current_time}")

with st.spinner("正在與國際伺服器抓取歷史數據..."):
    matches_data = fetch_live_scores()

if not matches_data:
    st.info("⚽ 找不到指定日期的賽事資料，請確認 API 金鑰或網路連線。")
else:
    st.success(f"✅ API 串接成功！獲取到 {len(matches_data)} 場賽事。")
    
    for match in matches_data:
        # 提取球隊名稱 (英文)
        home_team = match["teams"]["home"]["name"]
        away_team = match["teams"]["away"]["name"]
        
        # 提取比分
        home_score = match["goals"]["home"] or 0
        away_score = match["goals"]["away"] or 0
        
        # 比賽狀態 (PEN 代表進入 PK 戰結束)
        status_short = match["fixture"]["status"]["short"]
        
        st.markdown("---")
        col1, col2, col3 = st.columns([3, 1, 3])
        
        with col1:
            st.subheader(home_team) # 預期顯示 Argentina
        
        with col2:
            st.markdown(f"<h2 style='text-align: center; color: red;'>{home_score} - {away_score}</h2>", unsafe_allow_html=True)
            if status_short in ["FT", "AET", "PEN"]:
                st.markdown("<p style='text-align: center;'>比賽結束</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='text-align: center;'>{status_short}</p>", unsafe_allow_html=True)
                
        with col3:
            st.markdown(f"<h3 style='text-align: right;'>{away_team}</h3>", unsafe_allow_html=True) # 預期顯示 France

if st.button("🔄 手動強制刷新資料"):
    st.cache_data.clear()
    st.rerun()
