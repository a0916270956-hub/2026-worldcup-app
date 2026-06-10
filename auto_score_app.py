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

GROUP_MAP = {
    "GROUP_A": "A組", "GROUP_B": "B組", "GROUP_C": "C組", "GROUP_D": "D組",
    "GROUP_E": "E組", "GROUP_F": "F組", "GROUP_G": "G組", "GROUP_H": "H組",
    "GROUP_I": "I組", "GROUP_J": "J組", "GROUP_K": "K組", "GROUP_L": "L組"
}

# ==========================================
# 2. 核心數據抓取
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
        else:
            return {"error": f"錯誤代碼：{response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

@st.cache_data(ttl=60)
def fetch_standings():
    url = "https://api.football-data.org/v4/competitions/WC/standings"
    headers = {"X-Auth-Token": API_TOKEN}
    params = {"season": "2026"}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return {"data": response.json().get("standings", [])}
        else:
            return {"error": f"錯誤代碼：{response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_taipei_time(utc_date_str):
    try:
        utc_dt = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ")
        return utc_dt + timedelta(hours=8)
    except:
        return None

# ==========================================
# 3. 網頁介面
# ==========================================
st.set_page_config(page_title="世足賽即時看板(獨立版)", layout="centered")

st.title("🏆 2026 世足賽即時數據觀測台")

if st.button("🔄 強制同步最新數據", use_container_width=True):
    st.cache_data.clear()

sub_tab1, sub_tab2 = st.tabs(["📡 今日即時比分", "📊 各組積分表"])

# 【子分頁1：今日即時比分】
with sub_tab1:
    match_res = fetch_scores()
    if "error" in match_res:
        st.error(f"❌ 連線異常：{match_res['error']}")
    else:
        all_m = match_res.get("data", [])
        today_tpe = (datetime.utcnow() + timedelta(hours=8)).date()
        
        display_matches = [m for m in all_m if get_taipei_time(m.get("utcDate", "")) and get_taipei_time(m.get("utcDate", "")).date() == today_tpe]

        if not display_matches:
            st.info(f"⚽ 今日 ({today_tpe.strftime('%Y-%m-%d')}) 暫無世界盃賽事。\n(提示：2026世界盃首場分組賽將於台北時間 6/12 03:00 開踢！)")
        else:
            status_map = {"FINISHED": "比賽結束", "IN_PLAY": "進行中", "PAUSED": "中場休息", "TIMED": "未開始", "SCHEDULED": "已排程"}
            for match in display_matches:
                home = TEAM_TRANSLATION.get(match["homeTeam"]["name"], match["homeTeam"]["name"])
                away = TEAM_TRANSLATION.get(match["awayTeam"]["name"], match["awayTeam"]["name"])
                h_score = match["score"]["fullTime"]["home"] or 0
                a_score = match["score"]["fullTime"]["away"] or 0
                status_text = status_map.get(match["status"], match["status"])
                
                tpe_dt = get_taipei_time(match.get("utcDate", ""))
                time_str = tpe_dt.strftime("%H:%M") if tpe_dt else ""
                
                st.markdown("---")
                st.markdown(f"### 🏟️ {home} 🆚 {away} <span style='font-size: 14px; color: gray;'>({time_str} 開踢)</span>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                c1.metric(label=home, value=h_score)
                c2.metric(label="賽事狀態", value=status_text)
                c3.metric(label=away, value=a_score)

# 【子分頁2：各組積分表】
with sub_tab2:
    st.subheader("小組最新積分排行榜")
    stand_res = fetch_standings()
    if "error" in stand_res:
        st.error(f"❌ 無法讀取積分：{stand_res['error']}")
    else:
        standings_data = stand_res.get("data", [])
        if not standings_data:
            st.info("⚽ 暫無積分數據。")
        else:
            for group_data in standings_data:
                g_name = GROUP_MAP.get(group_data.get("group"), group_data.get("group"))
                st.write(f"#### 📍 {g_name}")
                table_rows = []
                for entry in group_data.get("table", []):
                    team_zh = TEAM_TRANSLATION.get(entry["team"]["name"], entry["team"]["name"])
                    table_rows.append({
                        "排名": entry.get("position"), "球隊": team_zh, "已賽": entry.get("playedGames"),
                        "勝": entry.get("won"), "和": entry.get("draw"), "敗": entry.get("lost"),
                        "積分": entry.get("points")
                    })
                st.dataframe(table_rows, use_container_width=True, hide_index=True)
