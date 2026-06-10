import streamlit as st
import requests
from datetime import datetime, timedelta

# ==========================================
# 1. API 設定區
# ==========================================
API_TOKEN = "d5921a999fd5418aa3c5026db3889cf2"

TEAM_TRANSLATION = {
    "Mexico": "墨西哥", "South Africa": "南非", "South Korea": "韓國", "Czech Republic": "捷克",
    "Canada": "加拿大", "Bosnia and Herzegovina": "波赫", "Qatar": "卡達", "Switzerland": "瑞士",
    "Brazil": "巴西", "Morocco": "摩洛哥", "Haiti": "海地", "Scotland": "蘇格蘭",
    "USA": "美國", "Paraguay": "巴拉圭", "Australia": "澳大利亞", "Turkey": "土耳其",
    "Germany": "德國", "Curaçao": "古拉索", "Ivory Coast": "象牙海岸", "Ecuador": "厄瓜多",
    "Netherlands": "荷蘭", "Japan": "日本", "Sweden": "瑞典", "Tunisia": "突尼西亞",
    "Belgium": "比利時", "Egypt": "埃及", "Iran": "伊朗", "New Zealand": "紐西蘭",
    "Spain": "西班牙", "Cape Verde": "維德角", "Saudi Arabia": "沙烏地", "Uruguay": "烏拉圭",
    "France": "法國", "Senegal": "塞內加爾", "Iraq": "伊拉克", "Norway": "挪威",
    "Argentina": "阿根廷", "Algeria": "阿爾及利亞", "Austria": "奧地利", "Jordan": "約旦",
    "Portugal": "葡萄牙", "Congo DR": "剛果", "Uzbekistan": "烏茲別克", "Colombia": "哥倫比亞",
    "England": "英格蘭", "Croatia": "克羅埃西亞", "Ghana": "迦納", "Panama": "巴拿馬"
}

# ==========================================
# 2. 核心功能與時間處理
# ==========================================
@st.cache_data(ttl=60)
def fetch_scores():
    url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": API_TOKEN}
    params = {"season": "2026"}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return {"data": response.json().get("matches", [])}
        elif response.status_code == 429:
            return {"error": "已達到每分鐘請求次數限制，請稍候再刷新。"}
        else:
            return {"error": f"國際伺服器回應錯誤 (代碼 {response.status_code})"}
    except Exception as e:
        return {"error": f"系統連線異常：{e}"}

def get_taipei_time(utc_date_str):
    try:
        utc_dt = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ")
        return utc_dt + timedelta(hours=8)
    except:
        return None

# ==========================================
# 3. 網頁介面
# ==========================================
st.set_page_config(page_title="世足賽即時比分", layout="centered")

st.title("🏆 2026 世足賽即時比分看板")
st.markdown("本系統已連線國際 API，所有賽程皆自動換算為 **台北時間 (UTC+8)**")

if st.button("🔄 手動強制刷新", use_container_width=True):
    st.cache_data.clear()

result = fetch_scores()

if "error" in result:
    st.error(f"❌ {result['error']}")
else:
    all_matches = result.get("data", [])
    
    # 計算台北時間的今日日期
    today_tpe_date = (datetime.utcnow() + timedelta(hours=8)).date()
    
    # 篩選今日賽事
    display_matches = []
    for m in all_matches:
        m_tpe_dt = get_taipei_time(m.get("utcDate", ""))
        if m_tpe_dt and m_tpe_dt.date() == today_tpe_date:
            display_matches.append(m)

    if not display_matches:
        st.info(f"⚽ 台北時間今日 ({today_tpe_date.strftime('%Y-%m-%d')}) 暫無世界盃賽事。\n(提示：2026世界盃首場分組賽將於台北時間 6/12 03:00 開踢！)")
    else:
        st.success(f"✅ 成功抓取 {len(display_matches)} 場資料！")
        
        status_map = {
            "FINISHED": "比賽結束", "IN_PLAY": "進行中", "PAUSED": "中場休息",
            "TIMED": "未開始", "SCHEDULED": "已排程", "POSTPONED": "延期"
        }
        
        for match in display_matches:
            home_en = match.get("homeTeam", {}).get("name", "未知名稱")
            away_en = match.get("awayTeam", {}).get("name", "未知名稱")
            home = TEAM_TRANSLATION.get(home_en, home_en)
            away = TEAM_TRANSLATION.get(away_en, away_en)
            
            score_data = match.get("score", {}).get("fullTime", {})
            h_score = score_data.get("home")
            a_score = score_data.get("away")
            h_score = 0 if h_score is None else h_score
            a_score = 0 if a_score is None else a_score
            
            status_raw = match.get("status", "UNKNOWN")
            status_text = status_map.get(status_raw, status_raw)
            
            tpe_dt = get_taipei_time(match.get("utcDate", ""))
            time_str = tpe_dt.strftime("%H:%M") if tpe_dt else ""
            
            st.markdown("---")
            st.markdown(f"### 🏟️ {home} 🆚 {away} <span style='font-size: 16px; color: gray;'>({time_str} 開踢)</span>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            col1.metric(label=home, value=h_score)
            col2.metric(label="賽事狀態", value=status_text)
            col3.metric(label=away, value=a_score)
