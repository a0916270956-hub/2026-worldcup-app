import streamlit as st
import requests
from datetime import datetime

# ==========================================
# 1. 設定區 (請將您的 API Key 貼在下方)
# ==========================================
RAPID_API_KEY = "5048786a54mshe1078420ed5662ap154c43jsndcfb158f929a" 
API_HOST = "api-football-v1.p.rapidapi.com"

# ==========================================
# 2. 核心功能：連網抓取數據 (加入快取機制)
# ==========================================
# 使用 st.cache_data 裝飾器，設定 ttl=60 (Time To Live)，
# 代表這支函式每 60 秒內只會真正連網抓取一次，保護您的 API 免費額度。
@st.cache_data(ttl=60)
def fetch_live_scores():
    # 這是 API-Football 的賽事端點 (Endpoint)
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    # 參數設定：
    # league=1 通常是世界盃的代碼 (2026年需確認最終代碼)
    # season=2026 設定賽季
    # status=LIVE 代表只抓取「正在進行中」的比賽 (若要全抓可移除此參數)
    querystring = {"league": "1", "season": "2026", "live": "all"}
    
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        
        # 檢查伺服器是否正常回應 (HTTP 200)
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
st.set_page_config(page_title="自動更新: 世足即時比分", page_icon="📡")

st.title("📡 2026 世足賽即時比分看板")
st.markdown("本系統自動連線至 API-Football 伺服器，每分鐘同步最新賽況。")

# 顯示最後更新時間
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.caption(f"🔄 最後更新時間：{current_time}")

# 執行連網抓取函式
if RAPID_API_KEY == "請將您的_API_KEY_貼在這裡":
    st.warning("⚠️ 請先在程式碼第 8 行填入您的 RapidAPI Key，系統才能連網抓取資料！")
else:
    with st.spinner("正在與國際伺服器同步比分數據..."):
        matches_data = fetch_live_scores()

    if not matches_data:
        st.info("⚽ 目前沒有正在進行中的世足賽事，或賽季尚未開始。")
    else:
        st.success(f"✅ 成功獲取 {len(matches_data)} 場賽事資訊！")
        
        # 解析 JSON 資料並顯示在畫面上
        for match in matches_data:
            # 提取球隊名稱
            home_team = match["teams"]["home"]["name"]
            away_team = match["teams"]["away"]["name"]
            
            # 提取比分 (如果還沒進球，API 會回傳 None，我們將其轉換為 0)
            home_score = match["goals"]["home"] or 0
            away_score = match["goals"]["away"] or 0
            
            # 提取比賽進行時間 (例如：第 45 分鐘)
            elapsed_time = match["fixture"]["status"]["elapsed"]
            status_short = match["fixture"]["status"]["short"]
            
            # 使用 Streamlit 的 Columns 做出漂亮的記分板排版
            st.markdown("---")
            col1, col2, col3 = st.columns([3, 1, 3])
            
            with col1:
                st.subheader(home_team)
            
            with col2:
                # 顯示大大的比分與比賽狀態 (例如： 2 - 1)
                st.markdown(f"<h2 style='text-align: center; color: red;'>{home_score} - {away_score}</h2>", unsafe_allow_html=True)
                if status_short == "HT":
                    st.markdown("<p style='text-align: center;'>中場休息</p>", unsafe_allow_html=True)
                elif status_short == "FT":
                    st.markdown("<p style='text-align: center;'>比賽結束</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center;'>⏱️ {elapsed_time}'</p>", unsafe_allow_html=True)
                    
            with col3:
                st.markdown(f"<h3 style='text-align: right;'>{away_team}</h3>", unsafe_allow_html=True)

# 提供手動刷新的按鈕
if st.button("🔄 手動強制刷新資料"):
    st.cache_data.clear() # 清除快取，強制下次執行時重新連網
    st.rerun()