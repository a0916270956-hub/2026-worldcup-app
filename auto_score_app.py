import streamlit as st
import requests

# ==========================================
# 1. 設定區 (已綁定您的 API Key)
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
# 3. 網頁介面
# ==========================================
st.set_page_config(page_title="世足賽即時比分", page_icon="🏆", layout="centered")

st.title("🏆 世足賽即時比分看板")
st.markdown("自動連網獲取最新國際賽事數據。")

# 模式切換：測試(2022歷史) vs 正式(2026)
mode = st.radio("模式切換：", ["測試 (2022決賽)", "正式 (2026賽季)"], horizontal=True)

if mode == "測試 (2022決賽)":
    data = fetch_scores("2022", "2022-12-18")
else:
    data = fetch_scores("2026")

# 錯誤處理與顯示邏輯
if data is None:
    st.error("❌ 無法連線到 API，請檢查網路狀態或 API 金鑰權限。")
elif len(data) == 0:
    st.warning("⚽ 目前無比賽資料，或賽季尚未開始。")
else:
    st.success(f"✅ 成功抓取 {len(data)} 場資料！")
    
    for match in data:
        try:
            # 提取球隊名稱
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            
            # 提取比分，若尚未產生則設為 0
            h_score = match["goals"]["home"]
            a_score = match["goals"]["away"]
            h_score = 0 if h_score is None else h_score
            a_score = 0 if a_score is None else a_score
            
            # 提取比賽狀態
            status = match["fixture"]["status"]["short"]
            
            # 採用最穩定的置中卡片排版，確保手機絕對能顯示
            st.markdown("---")
            st.markdown(f"<h3 style='text-align: center; color: #1E88E5;'>{home} &nbsp;&nbsp;🆚&nbsp;&nbsp; {away}</h3>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; color: #D32F2F; font-size: 3rem;'>{h_score} : {a_score}</h1>", unsafe_allow_html=True)
            
            if status in ["FT", "AET", "PEN"]:
                st.markdown("<p style='text-align: center; color: gray;'>比賽已結束</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='text-align: center; color: gray;'>賽事狀態代碼: {status}</p>", unsafe_allow_html=True)
                
        except Exception as e:
            # 如果 API 改變了格式，這裡會印出明確的錯誤原因，而不是默默空白
            st.error(f"資料解析失敗，錯誤代碼：{e}")
            with st.expander("👉 點擊查看原始 API 回傳結構"):
                st.write(match)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 手動強制刷新", use_container_width=True):
    st.cache_data.clear()
    st.rerun()
