import streamlit as st
import requests
from datetime import datetime, timedelta

# ==========================================
# 1. API 設定區
# ==========================================
API_TOKEN = "d5921a999fd5418aa3c5026db3889cf2"

TEAM_TRANSLATION = {
    "Argentina": "阿根廷", "France": "法國", "Croatia": "克羅埃西亞", "Morocco": "摩洛哥",
    "Netherlands": "荷蘭", "England": "英格蘭", "Brazil": "巴西", "Portugal": "葡萄牙",
    "Japan": "日本", "Senegal": "塞內加爾", "Australia": "澳大利亞", "Switzerland": "瑞士",
    "Spain": "西班牙", "United States": "美國", "USA": "美國", "Poland": "波蘭",
    "Korea Republic": "韓國", "South Korea": "韓國", "Cameroon": "喀麥隆", "Uruguay": "烏拉圭",
    "Tunisia": "突尼西亞", "Mexico": "墨西哥", "Belgium": "比利時", "Ghana": "迦納",
    "Saudi Arabia": "沙烏地阿拉伯", "Iran": "伊朗", "Iran (Islamic Republic of)": "伊朗",
    "Costa Rica": "哥斯大黎加", "Denmark": "丹麥", "Serbia": "塞爾維亞", "Wales": "威爾斯",
    "Ecuador": "厄瓜多", "Qatar": "卡達", "Canada": "加拿大", "Germany": "德國",
    "Italy": "義大利", "Chile": "智利", "Colombia": "哥倫比亞", "Peru": "秘魯",
    "Sweden": "瑞典", "Nigeria": "奈及利亞", "Egypt": "埃及", "Algeria": "阿爾及利亞",
    "Côte d'Ivoire": "象牙海岸", "Ivory Coast": "象牙海岸", "Mali": "馬利",
    "Burkina Faso": "布吉納法索", "South Africa": "南非", "Congo DR": "剛果民主共和國",
    "DR Congo": "剛果民主共和國", "Bosnia and Herzegovina": "波赫", "Czechia": "捷克",
    "Czech Republic": "捷克", "Republic of Ireland": "愛爾蘭", "Northern Ireland": "北愛爾蘭",
    "Scotland": "蘇格蘭", "Austria": "奧地利", "Hungary": "匈牙利", "Slovakia": "斯洛伐克",
    "Paraguay": "巴拉圭", "Venezuela": "委內瑞拉", "Bolivia": "玻利維亞", "New Zealand": "紐西蘭",
    "Haiti": "海地", "Jamaica": "牙買加", "Honduras": "宏都拉斯", "El Salvador": "薩爾瓦多",
    "Panama": "巴拿馬", "Cuba": "古巴", "Trinidad and Tobago": "千里達及托巴哥",
    "Curaçao": "古拉索", "Iraq": "伊拉克", "Syria": "敘利亞", "United Arab Emirates": "阿聯酋",
    "Uzbekistan": "烏茲別克", "China PR": "中國", "Oman": "阿曼", "Bahrain": "巴林",
    "Jordan": "約旦", "Lebanon": "黎巴嫩", "Vietnam": "越南", "Thailand": "泰國",
    "Indonesia": "印尼", "Malaysia": "馬來西亞", "India": "印度", "Türkiye": "土耳其",
    "Turkey": "土耳其", "Greece": "希臘", "Romania": "羅馬尼亞", "Bulgaria": "保加利亞",
    "Ukraine": "烏克蘭", "Russia": "俄羅斯", "Iceland": "冰島", "Finland": "芬蘭",
    "Norway": "挪威", "Slovenia": "斯洛維尼亞", "Albania": "阿爾巴尼亞", 
    "North Macedonia": "北馬其頓", "Georgia": "喬治亞", "Armenia": "亞美尼亞", "Israel": "以色列",
    "Cape Verde": "維德角"
}

GROUP_MAP = {
    "GROUP_A": "A組", "GROUP_B": "B組", "GROUP_C": "C組", "GROUP_D": "D組",
    "GROUP_E": "E組", "GROUP_F": "F組", "GROUP_G": "G組", "GROUP_H": "H組",
    "GROUP_I": "I組", "GROUP_J": "J組", "GROUP_K": "K組", "GROUP_L": "L組"
}

STATUS_MAP = {
    "FINISHED": "比賽結束", "IN_PLAY": "進行中", "PAUSED": "中場休息",
    "TIMED": "未開始", "SCHEDULED": "已排程", "POSTPONED": "延期"
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

def display_match_item(match):
    home_en = match.get("homeTeam", {}).get("name") or "Unknown"
    away_en = match.get("awayTeam", {}).get("name") or "Unknown"
    
    home = TEAM_TRANSLATION.get(home_en.strip(), home_en)
    away = TEAM_TRANSLATION.get(away_en.strip(), away_en)
    
    score_obj = match.get("score", {}) or {}
    full_time = score_obj.get("fullTime", {}) or {}
    h_score = full_time.get("home")
    a_score = full_time.get("away")
    
    status_raw = match.get("status", "UNKNOWN")
    status_text = STATUS_MAP.get(status_raw, status_raw)
    
    tpe_dt = get_taipei_time(match.get("utcDate", ""))
    time_str = tpe_dt.strftime("%H:%M") if tpe_dt else ""
    
    st.markdown("---")
    st.markdown(f"### 🏟️ {home} 🆚 {away} <span style='font-size: 14px; color: gray;'>({time_str} 開踢)</span>", unsafe_allow_html=True)
    
    h_display = 0 if h_score is None else h_score
    a_display = 0 if a_score is None else a_score
    c1, c2, c3 = st.columns(3)
    c1.metric(label=home, value=h_display)
    c2.metric(label="賽事狀態", value=status_text)
    c3.metric(label=away, value=a_display)
    
    with st.expander("📊 查看賽事詳細統計數據"):
        ht = score_obj.get('halfTime', {}) or {}
        et = score_obj.get('extraTime', {}) or {}
        pk = score_obj.get('penalties', {}) or {}
        
        ht_str = f"{ht.get('home')} : {ht.get('away')}" if ht.get('home') is not None else "-"
        et_str = f"{et.get('home')} : {et.get('away')}" if et.get('home') is not None else "無"
        pk_str = f"{pk.get('home')} : {pk.get('away')}" if pk.get('home') is not None else "無"
        
        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("半場比分", ht_str)
        sc2.metric("延長賽", et_str)
        sc3.metric("PK 戰", pk_str)
        
        referees = match.get("referees", [])
        if referees:
            ref_names = "、".join([r.get("name", "") for r in referees])
            st.caption(f"👨‍⚖️ **執法裁判團**：{ref_names}")

# ==========================================
# 3. 網頁介面
# ==========================================
st.set_page_config(page_title="世足賽即時看板(獨立版)", layout="centered")

st.title("🏆 2026 世足賽即時數據觀測台")

if st.button("🔄 強制同步最新數據", use_container_width=True):
    st.cache_data.clear()

sub_tab1, sub_tab2 = st.tabs(["📡 今日即時比分", "📊 各組積分表"])

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
            for match in display_matches:
                display_match_item(match)

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
                    team_en = entry.get("team", {}).get("name") or "Unknown"
                    team_zh = TEAM_TRANSLATION.get(team_en.strip(), team_en)
                    
                    table_rows.append({
                        "排名": entry.get("position"), "球隊": team_zh, "已賽": entry.get("playedGames"),
                        "勝": entry.get("won"), "和": entry.get("draw"), "敗": entry.get("lost"),
                        "積分": entry.get("points")
                    })
                st.dataframe(table_rows, use_container_width=True, hide_index=True)
