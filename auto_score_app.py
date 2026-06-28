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
    "Italy": "義大利", "Chile": "智利", "Colombia": "哥聯比亞", "Peru": "秘魯",
    "Sweden": "瑞典", "Nigeria": "奈及利亞", "Egypt": "埃及", "Algeria": "阿爾及利亞",
    "Côte d'Ivoire": "象牙海岸", "Ivory Coast": "象牙海岸", "Mali": "馬利",
    "Burkina Faso": "布吉納法索", "South Africa": "南非", "Congo DR": "剛果民主共和國",
    "DR Congo": "剛果民主共和國", "Bosnia and Herzegovina": "波赫", "Bosnia-Herzegovina": "波赫", 
    "Czechia": "捷克", "Czech Republic": "捷克", "Republic of Ireland": "愛爾蘭", 
    "Northern Ireland": "北愛爾蘭", "Scotland": "蘇格蘭", "Austria": "奧地利", 
    "Hungary": "匈牙利", "Slovakia": "斯洛伐克", "Paraguay": "巴拉圭", 
    "Venezuela": "委內瑞拉", "Bolivia": "玻利維亞", "New Zealand": "紐西蘭",
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
    "Cape Verde": "維德角", "Cape Verde Islands": "維德角", "TBD": "待定"
}

TEAM_RANKING = {
    "Argentina": 1, "France": 2, "Belgium": 3, "England": 4, "Brazil": 5, "Portugal": 6, 
    "Netherlands": 7, "Spain": 8, "Italy": 9, "Croatia": 10, "United States": 11, "USA": 11, 
    "Colombia": 12, "Morocco": 13, "Mexico": 14, "Uruguay": 15, "Germany": 16, "Senegal": 17, 
    "Japan": 18, "Switzerland": 19, "Iran": 20, "Iran (Islamic Republic of)": 20, "Denmark": 21, 
    "Ukraine": 22, "Korea Republic": 23, "South Korea": 23, "Australia": 24, "Austria": 25, 
    "Sweden": 26, "Hungary": 27, "Wales": 28, "Poland": 29, "Nigeria": 30, "Ecuador": 31, 
    "Peru": 32, "Serbia": 33, "Qatar": 34, "Russia": 35, "Czechia": 36, "Czech Republic": 36, 
    "Egypt": 37, "Côte d'Ivoire": 38, "Ivory Coast": 38, "Scotland": 39, "Türkiye": 40, "Turkey": 40, 
    "Tunisia": 41, "Algeria": 43, "Mali": 44, "Panama": 45, "Romania": 46, "Norway": 47, "Slovakia": 48, 
    "Canada": 49, "Greece": 50, "Venezuela": 54, "Saudi Arabia": 53, "South Africa": 59, 
    "Republic of Ireland": 60, "Ghana": 68, "Iceland": 72, "Northern Ireland": 73, "Georgia": 75, 
    "Bulgaria": 83, "China PR": 88, "Syria": 89, "New Zealand": 104, "Bosnia and Herzegovina": 74,
    "Bosnia-Herzegovina": 74, "Cape Verde": 65, "Cape Verde Islands": 65
}

GROUP_MAP = {
    "GROUP_A": "A組", "GROUP_B": "B組", "GROUP_C": "C組", "GROUP_D": "D組",
    "GROUP_E": "E組", "GROUP_F": "F組", "GROUP_G": "G組", "GROUP_H": "H組",
    "GROUP_I": "I組", "GROUP_J": "J組", "GROUP_K": "K組", "GROUP_L": "L組"
}

STATUS_MAP = {
    "FINISHED": "已完賽", "IN_PLAY": "進行中", "PAUSED": "中場休息",
    "TIMED": "未開始", "SCHEDULED": "未開始", "POSTPONED": "延期"
}

def is_real_team(team_name):
    if not team_name: return False
    fake_keywords = ["TBD", "待定", "WINNER", "LOSER", "GROUP", "MATCH", "1ST", "2ND", "3RD", "晉級", "首名", "次名", "第三名", "勝者", "敗者", "UNKNOWN"]
    return not any(kw in str(team_name).upper() for kw in fake_keywords)

# ==========================================
# 2. 核心數據抓取與智慧預填
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
        return {"error": str(response.status_code)}
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
        return {"error": str(response.status_code)}
    except Exception as e:
        return {"error": str(e)}

def get_taipei_time(utc_date_str):
    try:
        utc_dt = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ")
        return utc_dt + timedelta(hours=8)
    except:
        return None

def get_group_team(standings_data, group_letter, pos, fallback):
    if not standings_data: return fallback
    for g in standings_data:
        grp_raw = str(g.get("group", "")).upper().replace(" ", "_")
        if grp_raw == f"GROUP_{group_letter}" or grp_raw == group_letter:
            table = g.get("table", [])
            if len(table) >= pos:
                t_name = table[pos-1].get("team", {}).get("name", "")
                if t_name: return t_name
    return fallback

def inject_live_knockout_teams(all_matches, standings_data):
    mock_r32 = [
        ("A", 1, "A組 首名", "待定 (小組第三)"), ("B", 2, "B組 次名", "C", 2, "C組 次名"),
        ("D", 1, "D組 首名", "待定 (小組第三)"), ("E", 2, "E組 次名", "F", 2, "F組 次名"),
        ("G", 1, "G組 首名", "待定 (小組第三)"), ("H", 2, "H組 次名", "I", 2, "I組 次名"),
        ("J", 1, "J組 首名", "待定 (小組第三)"), ("K", 2, "K組 次名", "L", 2, "L組 次名"),
        ("B", 1, "B組 首名", "待定 (小組第三)"), ("A", 2, "A組 次名", "D", 2, "D組 次名"),
        ("C", 1, "C組 首名", "待定 (小組第三)"), ("E", 1, "E組 首名", "H", 1, "H組 首名"),
        ("F", 1, "F組 首名", "待定 (小組第三)"), ("G", 2, "G組 次名", "J", 2, "J組 次名"),
        ("I", 1, "I組 首名", "待定 (小組第三)"), ("K", 1, "K組 首名", "L", 1, "L組 首名")
    ]
    l32_matches = [m for m in all_matches if m.get("stage") == "LAST_32"]
    l32_matches.sort(key=lambda x: x.get("utcDate") or "")
    
    for i, m in enumerate(l32_matches):
        if i < len(mock_r32):
            cfg = mock_r32[i]
            if len(cfg) == 4:
                g_h, p_h, m_h, m_a = cfg
                real_h = get_group_team(standings_data, g_h, p_h, m_h)
                real_a = m_a
            else:
                g_h, p_h, m_h, g_a, p_a, m_a = cfg
                real_h = get_group_team(standings_data, g_h, p_h, m_h)
                real_a = get_group_team(standings_data, g_a, p_a, m_a)
            
            if "homeTeam" not in m or m["homeTeam"] is None or not is_real_team(m.get("homeTeam", {}).get("name")):
                m["homeTeam"] = {"name": real_h}
            if "awayTeam" not in m or m["awayTeam"] is None or not is_real_team(m.get("awayTeam", {}).get("name")):
                m["awayTeam"] = {"name": real_a}

    fallback_map = {
        "LAST_16": "32強晉級隊", "QUARTER_FINALS": "16強晉級隊", 
        "SEMI_FINALS": "8強晉級隊", "FINAL": "準決賽勝者", "THIRD_PLACE": "準決賽敗者"
    }
    for m in all_matches:
        stage = m.get("stage")
        if stage in fallback_map:
            def_val = fallback_map[stage]
            if "homeTeam" not in m or m["homeTeam"] is None or not is_real_team(m.get("homeTeam", {}).get("name")):
                m["homeTeam"] = {"name": def_val}
            if "awayTeam" not in m or m["awayTeam"] is None or not is_real_team(m.get("awayTeam", {}).get("name")):
                m["awayTeam"] = {"name": def_val}

def get_mock_knockout_matches(standings_data):
    mock_matches = []
    mock_r32 = [
        ("A", 1, "A組 首名", "待定 (小組第三)"), ("B", 2, "B組 次名", "C", 2, "C組 次名"),
        ("D", 1, "D組 首名", "待定 (小組第三)"), ("E", 2, "E組 次名", "F", 2, "F組 次名"),
        ("G", 1, "G組 首名", "待定 (小組第三)"), ("H", 2, "H組 次名", "I", 2, "I組 次名"),
        ("J", 1, "J組 首名", "待定 (小組第三)"), ("K", 2, "K組 次名", "L", 2, "L組 次名"),
        ("B", 1, "B組 首名", "待定 (小組第三)"), ("A", 2, "A組 次名", "D", 2, "D組 次名"),
        ("C", 1, "C組 首名", "待定 (小組第三)"), ("E", 1, "E組 首名", "H", 1, "H組 首名"),
        ("F", 1, "F組 首名", "待定 (小組第三)"), ("G", 2, "G組 次名", "J", 2, "J組 次名"),
        ("I", 1, "I組 首名", "待定 (小組第三)"), ("K", 1, "K組 首名", "L", 1, "L組 首名")
    ]
    for cfg in mock_r32:
        if len(cfg) == 4:
            g_h, p_h, mock_h, mock_a = cfg
            h = get_group_team(standings_data, g_h, p_h, mock_h)
            a = mock_a
        else:
            g_h, p_h, mock_h, g_a, p_a, mock_a = cfg
            h = get_group_team(standings_data, g_h, p_h, mock_h)
            a = get_group_team(standings_data, g_a, p_a, mock_a)
        mock_matches.append({"stage": "LAST_32", "status": "SCHEDULED", "utcDate": "", "homeTeam": {"name": h}, "awayTeam": {"name": a}, "score": {"fullTime": {"home": None, "away": None}}})
    
    for _ in range(8):
        mock_matches.append({"stage": "LAST_16", "status": "SCHEDULED", "utcDate": "", "homeTeam": {"name": "32強晉級隊"}, "awayTeam": {"name": "32強晉級隊"}, "score": {"fullTime": {"home": None, "away": None}}})
    for _ in range(4):
        mock_matches.append({"stage": "QUARTER_FINALS", "status": "SCHEDULED", "utcDate": "", "homeTeam": {"name": "16強晉級隊"}, "awayTeam": {"name": "16強晉級隊"}, "score": {"fullTime": {"home": None, "away": None}}})
    for _ in range(2):
        mock_matches.append({"stage": "SEMI_FINALS", "status": "SCHEDULED", "utcDate": "", "homeTeam": {"name": "8強晉級隊"}, "awayTeam": {"name": "8強晉級隊"}, "score": {"fullTime": {"home": None, "away": None}}})
    mock_matches.append({"stage": "FINAL", "status": "SCHEDULED", "utcDate": "", "homeTeam": {"name": "準決賽勝者"}, "awayTeam": {"name": "準決賽勝者"}, "score": {"fullTime": {"home": None, "away": None}}})
    mock_matches.append({"stage": "THIRD_PLACE", "status": "SCHEDULED", "utcDate": "", "homeTeam": {"name": "準決賽敗者"}, "awayTeam": {"name": "準決賽敗者"}, "score": {"fullTime": {"home": None, "away": None}}})
    return mock_matches

def get_match_card_html(match):
    home_en = match.get("homeTeam", {}).get("name") or "TBD"
    away_en = match.get("awayTeam", {}).get("name") or "TBD"
    home = TEAM_TRANSLATION.get(home_en.strip(), home_en)
    away = TEAM_TRANSLATION.get(away_en.strip(), away_en)
    
    home_rank = TEAM_RANKING.get(home_en.strip(), "")
    away_rank = TEAM_RANKING.get(away_en.strip(), "")
    h_tag = f" <span style='font-size:10px; color:#a0a0a0;'>#{home_rank}</span>" if home_rank else ""
    a_tag = f" <span style='font-size:10px; color:#a0a0a0;'>#{away_rank}</span>" if away_rank else ""

    score_obj = match.get("score", {}) or {}
    full_time = score_obj.get("fullTime", {}) or {}
    h_score = full_time.get("home") if full_time.get("home") is not None else "-"
    a_score = full_time.get("away") if full_time.get("away") is not None else "-"

    tpe_dt = get_taipei_time(match.get("utcDate", ""))
    dt_display = tpe_dt.strftime("%m/%d %H:%M") if tpe_dt else "時間待定"

    html = (
        f'<div style="background-color: #ffffff; border: 1px solid #dadce0; border-radius: 8px; '
        f'padding: 6px 12px; margin: 2px 0; width: 175px; box-shadow: none; font-family: sans-serif;">'
        f'<div style="font-size: 11px; color: #70757a; margin-bottom: 4px; border-bottom: 1px solid #f1f3f4; padding-bottom: 2px;">{dt_display}</div>'
        f'<div style="display: flex; justify-content: space-between; align-items: center; height: 22px;">'
        f'<span style="font-size: 13px; font-weight: 500; color: #202124; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 135px;">{home}{h_tag}</span>'
        f'<span style="font-size: 13px; font-weight: bold; color: #202124;">{h_score}</span>'
        f'</div>'
        f'<div style="display: flex; justify-content: space-between; align-items: center; height: 22px;">'
        f'<span style="font-size: 13px; font-weight: 500; color: #202124; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 135px;">{away}{a_tag}</span>'
        f'<span style="font-size: 13px; font-weight: bold; color: #202124;">{a_score}</span>'
        f'</div>'
        f'</div>'
    )
    return html

def display_match_item(match):
    home_en = match.get("homeTeam", {}).get("name") or "TBD"
    away_en = match.get("awayTeam", {}).get("name") or "TBD"
    home = TEAM_TRANSLATION.get(home_en.strip(), home_en)
    away = TEAM_TRANSLATION.get(away_en.strip(), away_en)
    
    home_rank = TEAM_RANKING.get(home_en.strip(), "-")
    away_rank = TEAM_RANKING.get(away_en.strip(), "-")
    h_rank_tag = f" <span style='font-size: 13px; color: #1E88E5; font-weight:normal;'>(排:#{home_rank})</span>" if home_rank != "-" else ""
    a_rank_tag = f" <span style='font-size: 13px; color: #1E88E5; font-weight:normal;'>(排:#{away_rank})</span>" if away_rank != "-" else ""
    
    score_obj = match.get("score", {}) or {}
    full_time = score_obj.get("fullTime", {}) or {}
    h_score = full_time.get("home")
    a_score = full_time.get("away")
    
    status_raw = match.get("status", "UNKNOWN")
    status_text = STATUS_MAP.get(status_raw, status_raw)
    tpe_dt = get_taipei_time(match.get("utcDate", ""))
    time_str = tpe_dt.strftime("%H:%M") if tpe_dt else "時間待定"
    
    st.markdown("---")
    st.markdown(f"### 🏟️ {home}{h_rank_tag} 🆚 {away}{a_rank_tag} <span style='font-size: 14px; color: gray; margin-left:10px;'>({time_str} 開踢)</span>", unsafe_allow_html=True)
    
    h_display = "-" if h_score is None else h_score
    a_display = "-" if a_score is None else a_score
    
    c1, c2, c3 = st.columns(3)
    c1.metric(label=home, value=h_display)
    c2.metric(label="賽事狀態", value=status_text)
    c3.metric(label=away, value=a_display)

# ==========================================
# 3. 網頁介面
# ==========================================
st.set_page_config(page_title="世足賽即時看板(獨立版)", layout="wide")
st.title("🏆 2026 世足賽即時數據觀測台")

if st.button("🔄 強制同步最新數據", use_container_width=True):
    st.cache_data.clear()

sub_tab1, sub_tab2, sub_tab3 = st.tabs(["🌳 晉級樹狀圖", "📡 今日與次日賽程", "📊 各組積分與數據"])

match_res = fetch_scores()
stand_res = fetch_standings()

if "error" not in match_res:
    all_m = match_res.get("data", [])
    standings_data = stand_res.get("data", []) if "error" not in stand_res else []
    
    ko_stages = ["LAST_32", "LAST_16", "QUARTER_FINALS", "SEMI_FINALS", "THIRD_PLACE", "FINAL"]
    ko_matches = [m for m in all_m if m.get("stage") in ko_stages]
    
    if not ko_matches:
        all_m.extend(get_mock_knockout_matches(standings_data))
    else:
        inject_live_knockout_teams(all_m, standings_data)

with sub_tab1:
    st.subheader("🌳 淘汰賽晉級樹狀圖 (仿 Google 網格流)")
    tree_stages = ["LAST_32", "LAST_16", "QUARTER_FINALS", "SEMI_FINALS", "FINAL", "THIRD_PLACE"]
    tree_matches = [m for m in all_m if m.get("stage") in tree_stages]
    
    col_html = {"LAST_32": "", "LAST_16": "", "QUARTER_FINALS": "", "SEMI_FINALS": "", "FINAL": "", "THIRD_PLACE": ""}
    for m in tree_matches:
        stage = m.get("stage")
        if stage in col_html:
            col_html[stage] += get_match_card_html(m)
            
    bracket_html = (
        '<div style="overflow-x: auto; background-color: #ffffff; padding: 15px; border: 1px solid #dadce0; border-radius: 12px; margin-top: 10px;">'
        '<div style="display: flex; min-width: 1050px; gap: 15px; border-bottom: 1px solid #f1f3f4; padding-bottom: 8px; margin-bottom: 12px;">'
        '<div style="flex: 1; text-align: center; font-weight: bold; color: #70757a; font-size: 13px;">32強賽</div>'
        '<div style="flex: 1; text-align: center; font-weight: bold; color: #70757a; font-size: 13px;">16強賽</div>'
        '<div style="flex: 1; text-align: center; font-weight: bold; color: #70757a; font-size: 13px;">8強賽</div>'
        '<div style="flex: 1; text-align: center; font-weight: bold; color: #70757a; font-size: 13px;">4強賽</div>'
        '<div style="flex: 1; text-align: center; font-weight: bold; color: #ff8f00; font-size: 13px;">決賽階段</div>'
        '</div>'
        '<div style="display: flex; min-width: 1050px; height: 1100px; gap: 15px;">'
        f'<div style="flex: 1; display: flex; flex-direction: column; justify-content: space-around; height: 100%;">{col_html["LAST_32"]}</div>'
        f'<div style="flex: 1; display: flex; flex-direction: column; justify-content: space-around; height: 100%;">{col_html["LAST_16"]}</div>'
        f'<div style="flex: 1; display: flex; flex-direction: column; justify-content: space-around; height: 100%;">{col_html["QUARTER_FINALS"]}</div>'
        f'<div style="flex: 1; display: flex; flex-direction: column; justify-content: space-around; height: 100%;">{col_html["SEMI_FINALS"]}</div>'
        f'<div style="flex: 1; display: flex; flex-direction: column; justify-content: space-around; height: 100%; border-left: 1px dashed #dadce0; padding-left: 8px;">'
        f'<div><div style="font-size:11px; color:#ff8f00; font-weight:bold; margin-bottom:2px; text-align:center;">🏆 冠軍戰</div>{col_html["FINAL"]}</div>'
        f'<div><div style="font-size:11px; color:#70757a; font-weight:bold; margin-bottom:2px; text-align:center;">🥉 季軍戰</div>{col_html["THIRD_PLACE"]}</div>'
        f'</div>'
        '</div></div>'
    )
    st.markdown(bracket_html, unsafe_allow_html=True)

with sub_tab2:
    today_tpe_date = (datetime.utcnow() + timedelta(hours=8)).date()
    tomorrow_tpe_date = today_tpe_date + timedelta(days=1)
    today_matches = []
    tomorrow_matches = []
    for m in all_m:
        m_tpe_dt = get_taipei_time(m.get("utcDate", ""))
        if m_tpe_dt:
            if m_tpe_dt.date() == today_tpe_date: today_matches.append(m)
            elif m_tpe_dt.date() == tomorrow_tpe_date: tomorrow_matches.append(m)

    st.subheader(f"🔥 今日賽事 ({today_tpe_date.strftime('%m/%d')})")
    if today_matches:
        for match in today_matches: display_match_item(match)
    else: st.info("⚽ 今日暫無世界盃賽事。")
            
    st.subheader(f"🔜 明日預告 ({tomorrow_tpe_date.strftime('%m/%d')})")
    if tomorrow_matches:
        for match in tomorrow_matches: display_match_item(match)
    else: st.info("⚽ 明日暫無賽事安排。")

with sub_tab3:
    st.subheader("小組最新積分與詳細數據統計")
    if "error" not in stand_res:
        standings_data_table = stand_res.get("data", [])
        for group_data in standings_data_table:
            g_name = GROUP_MAP.get(group_data.get("group"), group_data.get("group"))
            st.write(f"#### 📍 {g_name}")
            table_rows = []
            for entry in group_data.get("table", []):
                team_en = entry.get("team", {}).get("name") or "TBD"
                team_zh = TEAM_TRANSLATION.get(team_en.strip(), team_en)
                table_rows.append({
                    "排名": entry.get("position"), "球隊": team_zh, "已賽": entry.get("playedGames"),
                    "勝": entry.get("won"), "和": entry.get("draw"), "敗": entry.get("lost"),
                    "進/失球": f"{entry.get('goalsFor')} / {entry.get('goalsAgainst')}",
                    "淨勝球(GD)": entry.get("goalDifference"), "總積分": entry.get("points")
                })
            st.dataframe(table_rows, use_container_width=True, hide_index=True)
