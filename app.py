import streamlit as st
import requests
from datetime import datetime, timedelta

# ==========================================
# 1. API 設定區
# ==========================================
API_TOKEN = "d5921a999fd5418aa3c5026db3889cf2"

# 🌟 全面擴充的全球球隊中英文名稱翻譯字典 (涵蓋 FIFA 所有可能別名)
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

STATUS_MAP = {
    "FINISHED": "比賽結束", "IN_PLAY": "進行中", "PAUSED": "中場休息",
    "TIMED": "未開始", "SCHEDULED": "已排程", "POSTPONED": "延期"
}

STAGE_MAP = {
    "FINAL": "🏆 冠軍總決賽", "THIRD_PLACE": "🥉 季軍爭奪戰", "SEMI_FINALS": "⭐ 4強準決賽",
    "QUARTER_FINALS": "⚔️ 8強半決賽", "LAST_16": "🎯 16強淘汰賽", "LAST_32": "🚀 32強淘汰賽",
    "GROUP_STAGE": "⚽ 分組賽段"
}

GROUP_MAP = {
    "GROUP_A": "A組", "GROUP_B": "B組", "GROUP_C": "C組", "GROUP_D": "D組",
    "GROUP_E": "E組", "GROUP_F": "F組", "GROUP_G": "G組", "GROUP_H": "H組",
    "GROUP_I": "I組", "GROUP_J": "J組", "GROUP_K": "K組", "GROUP_L": "L組"
}

# ==========================================
# 2. 自動連網抓取與時間轉換函式
# ==========================================
@st.cache_data(ttl=60)
def fetch_all_matches():
    url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": API_TOKEN}
    params = {"season": "2026"}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return {"data": response.json().get("matches", [])}
        elif response.status_code == 429:
            return {"error": "已達到每分鐘請求次數限制，請等候一分鐘後再刷新。"}
        else:
            return {"error": f"國際伺服器賽程回應錯誤 (代碼 {response.status_code})"}
    except Exception as e:
        return {"error": f"系統連線異常：{e}"}

@st.cache_data(ttl=60)
def fetch_standings():
    url = "https://api.football-data.org/v4/competitions/WC/standings"
    headers = {"X-Auth-Token": API_TOKEN}
    params = {"season": "2026"}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return {"data": response.json().get("standings", [])}
        elif response.status_code == 429:
            return {"error": "已達到每分鐘請求次數限制，請等候一分鐘。"}
        else:
            return {"error": f"國際伺服器積分回應錯誤 (代碼 {response.status_code})"}
    except Exception as e:
        return {"error": f"積分連線異常：{e}"}

def get_taipei_time(utc_date_str):
    try:
        utc_dt = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ")
        return utc_dt + timedelta(hours=8)
    except:
        return None

# ==========================================
# 3. UI 模組：賽事卡片與詳細數據渲染
# ==========================================
def display_match_item(match, is_today=False):
    home_en = match.get("homeTeam", {}).get("name") or "Unknown"
    away_en = match.get("awayTeam", {}).get("name") or "Unknown"
    
    # 確保翻譯精準對應
    home = TEAM_TRANSLATION.get(home_en.strip(), home_en)
    away = TEAM_TRANSLATION.get(away_en.strip(), away_en)
    
    score_obj = match.get("score", {}) or {}
    full_time = score_obj.get("fullTime", {}) or {}
    h_score = full_time.get("home")
    a_score = full_time.get("away")
    
    status_raw = match.get("status", "UNKNOWN")
    status_text = STATUS_MAP.get(status_raw, status_raw)
    
    tpe_dt = get_taipei_time(match.get("utcDate", ""))
    
    st.markdown("---")
    if is_today:
        time_str = tpe_dt.strftime("%H:%M") if tpe_dt else ""
        st.markdown(f"### 🏟️ {home} 🆚 {away} <span style='font-size: 14px; color: gray;'>({time_str} 台北時間開踢)</span>", unsafe_allow_html=True)
    else:
        dt_display = tpe_dt.strftime("%m/%d %H:%M") if tpe_dt else match.get("utcDate", "")
        st.markdown(f"### 🏟️ {home} 🆚 {away} <span style='font-size: 14px; color: gray;'>({dt_display})</span>", unsafe_allow_html=True)

    # 主要比分看板
    h_display = 0 if h_score is None else h_score
    a_display = 0 if a_score is None else a_score
    col1, col2, col3 = st.columns(3)
    col1.metric(label=home, value=h_display)
    col2.metric(label="賽事狀態", value=status_text)
    col3.metric(label=away, value=a_display)
    
    # 📊 詳細數據展開選單
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
        
        st.caption("💡 提示：其他進階統計需視官方伺服器釋出狀況更新。")

# ==========================================
# 4. 主程式排版
# ==========================================
st.set_page_config(page_title="2026世足動態全功能看板", page_icon="🏆", layout="centered")

st.title("🏆 2026 世足賽動態看板")
st.markdown("美加墨聯合主辦｜賽程・即時比分・分組積分全自動同步系統")

if st.button("🔄 立即刷新、同步最新數據", use_container_width=True):
    st.cache_data.clear()

matches_result = fetch_all_matches()
standings_result = fetch_standings()

if "error" in matches_result:
    st.error(f"❌ 賽程載入失敗：{matches_result['error']}")
else:
    all_matches = matches_result.get("data", [])
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 淘汰賽戰況", "⚽ 分組賽進度", "📊 各組積分表", "📡 今日即時焦點"])
    
    # 【分頁1：淘汰賽】
    with tab1:
        st.subheader("世界盃淘汰賽最新戰況")
        ko_stages = ["LAST_32", "LAST_16", "QUARTER_FINALS", "SEMI_FINALS", "THIRD_PLACE", "FINAL"]
        ko_matches = [m for m in all_matches if m.get("stage") in ko_stages]
        
        if not ko_matches:
            st.info("⚽ 淘汰賽組合將於分組賽結束後由官方自動生成。")
        else:
            for stage_code in reversed(ko_stages):
                stage_matches = [m for m in ko_matches if m.get("stage") == stage_code]
                if stage_matches:
                    with st.expander(STAGE_MAP.get(stage_code, stage_code)):
                        for m in stage_matches:
                            display_match_item(m, is_today=False)

    # 【分頁2：分組賽】
    with tab2:
        st.subheader("48強分組賽動態賽程")
        g_matches_list = [m for m in all_matches if m.get("stage") == "GROUP_STAGE"]
        
        if not g_matches_list:
            st.info("⚽ 目前伺服器暫無分組賽程數據。")
        else:
            all_groups = sorted(list(set([m.get("group") for m in g_matches_list if m.get("group")])))
            for g_code in all_groups:
                g_matches = [m for m in g_matches_list if m.get("group") == g_code]
                with st.expander(f"📍 {GROUP_MAP.get(g_code, g_code)} 賽程進度"):
                    for m in g_matches:
                        display_match_item(m, is_today=False)

    # 【分頁3：積分表】
    with tab3:
        st.subheader("2026 世界盃小組積分榜")
        if "error" in standings_result:
            st.error(f"❌ 積分表同步失敗：{standings_result['error']}")
        else:
            standings_data = standings_result.get("data", [])
            if not standings_data:
                st.info("⚽ 官方尚未上傳分組積分表數據。")
            else:
                for group_data in standings_data:
                    g_code = group_data.get("group")
                    g_name = GROUP_MAP.get(g_code, g_code)
                    
                    st.write(f"#### 📍 {g_name}")
                    table_rows = []
                    for entry in group_data.get("table", []):
                        team_en = entry.get("team", {}).get("name") or "Unknown"
                        team_zh = TEAM_TRANSLATION.get(team_en.strip(), team_en)
                        
                        table_rows.append({
                            "排名": entry.get("position"),
                            "球隊": team_zh,
                            "已賽": entry.get("playedGames"),
                            "勝": entry.get("won"),
                            "和": entry.get("draw"),
                            "敗": entry.get("lost"),
                            "進球/失球": f"{entry.get('goalsFor')} / {entry.get('goalsAgainst')}",
                            "得失差": entry.get("goalDifference"),
                            "積分": entry.get("points")
                        })
                    st.dataframe(table_rows, use_container_width=True, hide_index=True)

    # 【分頁4：今日即時焦點】
    with tab4:
        st.subheader("開源伺服器當日同步")
        today_tpe_date = (datetime.utcnow() + timedelta(hours=8)).date()
        
        today_matches = []
        for m in all_matches:
            m_tpe_dt = get_taipei_time(m.get("utcDate", ""))
            if m_tpe_dt and m_tpe_dt.date() == today_tpe_date:
                today_matches.append(m)
            
        if not today_matches:
            st.info(f"⚽ 台北時間今日 ({today_tpe_date.strftime('%Y-%m-%d')}) 暫無進行中的世界盃賽事。\n(提示：2026世界盃首場分組賽將於台北時間 6/12 03:00 正式開踢！)")
        else:
            st.success(f"✅ 成功同步今日 {len(today_matches)} 場賽事！")
            for match in today_matches:
                display_match_item(match, is_today=True)
