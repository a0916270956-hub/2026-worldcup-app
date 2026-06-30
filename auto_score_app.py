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

TEAM_FLAG_CODE = {
    "Argentina": "ar", "France": "fr", "Croatia": "hr", "Morocco": "ma",
    "Netherlands": "nl", "England": "gb-eng", "Brazil": "br", "Portugal": "pt",
    "Japan": "jp", "Senegal": "sn", "Australia": "au", "Switzerland": "ch",
    "Spain": "es", "United States": "us", "USA": "us", "Poland": "pl",
    "Korea Republic": "kr", "South Korea": "kr", "Cameroon": "cm", "Uruguay": "uy",
    "Tunisia": "tn", "Mexico": "mx", "Belgium": "be", "Ghana": "gh",
    "Saudi Arabia": "sa", "Iran": "ir", "Iran (Islamic Republic of)": "ir",
    "Costa Rica": "cr", "Denmark": "dk", "Serbia": "rs", "Wales": "gb-wls",
    "Ecuador": "ec", "Qatar": "qa", "Canada": "ca", "Germany": "de",
    "Italy": "it", "Chile": "cl", "Colombia": "co", "Peru": "pe",
    "Sweden": "se", "Nigeria": "ng", "Egypt": "eg", "Algeria": "dz",
    "Côte d'Ivoire": "ci", "Ivory Coast": "ci", "Mali": "ml",
    "Burkina Faso": "bf", "South Africa": "za", "Congo DR": "cd",
    "DR Congo": "cd", "Bosnia and Herzegovina": "ba", "Bosnia-Herzegovina": "ba", 
    "Czechia": "cz", "Czech Republic": "cz", "Republic of Ireland": "ie", "Ireland": "ie",
    "Northern Ireland": "gb-nir", "Scotland": "gb-sct", "Austria": "at", 
    "Hungary": "hu", "Slovakia": "sk", "Paraguay": "py", 
    "Venezuela": "ve", "Bolivia": "bo", "New Zealand": "nz",
    "Haiti": "ht", "Jamaica": "jm", "Honduras": "hn", "El Salvador": "sv",
    "Panama": "pa", "Cuba": "cu", "Trinidad and Tobago": "tt",
    "Curaçao": "cw", "Iraq": "iq", "Syria": "sy", "United Arab Emirates": "ae",
    "Uzbekistan": "uz", "China PR": "cn", "Oman": "om", "Bahrain": "bh",
    "Jordan": "jo", "Lebanon": "lb", "Vietnam": "vn", "Thailand": "th",
    "Indonesia": "id", "Malaysia": "my", "India": "in", "Türkiye": "tr",
    "Turkey": "tr", "Greece": "gr", "Romania": "ro", "Bulgaria": "bg",
    "Ukraine": "ua", "Russia": "ru", "Iceland": "is", "Finland": "fi",
    "Norway": "no", "Slovenia": "si", "Albania": "al", 
    "North Macedonia": "mk", "Georgia": "ge", "Armenia": "am", "Israel": "il",
    "Cape Verde": "cv", "Cape Verde Islands": "cv", "Kosovo": "xk",
    "Montenegro": "me", "Guinea": "gn", "Gabon": "ga", "Benin": "bj"
}

TEAM_RANKING = {
    "Argentina": 1, "Spain": 2, "France": 3, "England": 4, "Portugal": 5,
    "Brazil": 6, "Morocco": 7, "Netherlands": 8, "Belgium": 9, "Germany": 10,
    "Croatia": 11, "Italy": 12, "Colombia": 13, "Mexico": 14, "Senegal": 15,
    "Uruguay": 16, "USA": 17, "United States": 17, "Japan": 18, "Switzerland": 19,
    "Iran": 20, "Iran (Islamic Republic of)": 20, "Denmark": 21, "Türkiye": 22, "Turkey": 22,
    "Ecuador": 23, "Austria": 24, "South Korea": 25, "Korea Republic": 25, 
    "Nigeria": 26, "Australia": 27, "Algeria": 28, "Egypt": 29, "Canada": 30,
    "Norway": 31, "Ukraine": 32, "Côte d'Ivoire": 33, "Ivory Coast": 33,
    "Panama": 34, "Russia": 35, "Poland": 36, "Wales": 37, "Sweden": 38,
    "Hungary": 39, "Czechia": 40, "Czech Republic": 40, "Paraguay": 41,
    "Scotland": 42, "Serbia": 43, "Cameroon": 44, "Tunisia": 45,
    "DR Congo": 46, "Congo DR": 46, "Slovakia": 47, "Greece": 48,
    "Venezuela": 49, "Uzbekistan": 50, "Chile": 51, "Peru": 52,
    "Costa Rica": 53, "Romania": 54, "Mali": 55, "Qatar": 56, "Iraq": 57,
    "Republic of Ireland": 58, "Ireland": 58, "Slovenia": 59, "South Africa": 60,
    "Saudi Arabia": 61, "Burkina Faso": 62, "Jordan": 63, "Bosnia and Herzegovina": 64,
    "Bosnia-Herzegovina": 64, "Honduras": 65, "Albania": 66, "Cape Verde": 67, 
    "Cape Verde Islands": 67, "United Arab Emirates": 68, "North Macedonia": 69, 
    "Northern Ireland": 70, "Jamaica": 71, "Georgia": 72, "Ghana": 73, "Iceland": 74, 
    "Finland": 75, "Israel": 76, "Bolivia": 77, "Kosovo": 78, "Oman": 79, "Montenegro": 80,
    "Guinea": 81, "Curaçao": 82, "Haiti": 83, "Syria": 84, "New Zealand": 85,
    "Gabon": 86, "Bulgaria": 87, "China PR": 91, "Benin": 93, "Lebanon": 115
}

STATUS_MAP = {
    "FINISHED": "已完賽", "IN_PLAY": "進行中", "PAUSED": "中場休息",
    "TIMED": "未開始", "SCHEDULED": "未開始", "POSTPONED": "延期"
}

GROUP_MAP = {
    "GROUP_A": "A組", "GROUP_B": "B組", "GROUP_C": "C組", "GROUP_D": "D組",
    "GROUP_E": "E組", "GROUP_F": "F組", "GROUP_G": "G組", "GROUP_H": "H組",
    "GROUP_I": "I組", "GROUP_J": "J組", "GROUP_K": "K組", "GROUP_L": "L組"
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

def get_mock_date(stage, index):
    base_dates = {
        "LAST_32": datetime(2026, 6, 28, 12, 0, 0),
        "LAST_16": datetime(2026, 7, 4, 12, 0, 0),
        "QUARTER_FINALS": datetime(2026, 7, 9, 12, 0, 0),
        "SEMI_FINALS": datetime(2026, 7, 14, 16, 0, 0),
        "THIRD_PLACE": datetime(2026, 7, 18, 16, 0, 0),
        "FINAL": datetime(2026, 7, 19, 16, 0, 0)
    }
    base = base_dates.get(stage, datetime(2026, 6, 28, 0, 0, 0))
    if stage in ["LAST_32", "LAST_16", "QUARTER_FINALS"]:
        offset = timedelta(days=index // 2, hours=(index % 2) * 4)
    elif stage == "SEMI_FINALS":
        offset = timedelta(days=index, hours=0)
    else:
        offset = timedelta(0)
    return (base + offset).strftime("%Y-%m-%dT%H:%M:%SZ")

def inject_live_knockout_teams(all_matches, standings_data):
    mock_r32 = [
        ("A", 1, "A組 首名", "待定(小組第三)"), ("B", 2, "B組 次名", "C", 2, "C組 次名"),
        ("D", 1, "D組 首名", "待定(小組第三)"), ("E", 2, "E組 次名", "F", 2, "F組 次名"),
        ("G", 1, "G組 首名", "待定(小組第三)"), ("H", 2, "H組 次名", "I", 2, "I組 次名"),
        ("J", 1, "J組 首名", "待定(小組第三)"), ("K", 2, "K組 次名", "L", 2, "L組 次名"),
        ("B", 1, "B組 首名", "待定(小組第三)"), ("A", 2, "A組 次名", "D", 2, "D組 次名"),
        ("C", 1, "C組 首名", "待定(小組第三)"), ("E", 1, "E組 首名", "H", 1, "H組 首名"),
        ("F", 1, "F組 首名", "待定(小組第三)"), ("G", 2, "G組 次名", "J", 2, "J組 次名"),
        ("I", 1, "I組 首名", "待定(小組第三)"), ("K", 1, "K組 首名", "L", 1, "L組 首名")
    ]
    l32_matches = [m for m in all_matches if m.get("stage") == "LAST_32"]
    # 【關鍵修正】: 取消以時間排序，確保樹狀圖配對路線正確
    l32_matches.sort(key=lambda x: x.get("id", 0))
    
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
        "LAST_16": "32強勝者", "QUARTER_FINALS": "16強勝者", 
        "SEMI_FINALS": "8強勝者", "FINAL": "準決賽勝者", "THIRD_PLACE": "準決賽敗者"
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
        ("A", 1, "A組 首名", "待定(小組第三)"), ("B", 2, "B組 次名", "C", 2, "C組 次名"),
        ("D", 1, "D組 首名", "待定(小組第三)"), ("E", 2, "E組 次名", "F", 2, "F組 次名"),
        ("G", 1, "G組 首名", "待定(小組第三)"), ("H", 2, "H組 次名", "I", 2, "I組 次名"),
        ("J", 1, "J組 首名", "待定(小組第三)"), ("K", 2, "K組 次名", "L", 2, "L組 次名"),
        ("B", 1, "B組 首名", "待定(小組第三)"), ("A", 2, "A組 次名", "D", 2, "D組 次名"),
        ("C", 1, "C組 首名", "待定(小組第三)"), ("E", 1, "E組 首名", "H", 1, "H組 首名"),
        ("F", 1, "F組 首名", "待定(小組第三)"), ("G", 2, "G組 次名", "J", 2, "J組 次名"),
        ("I", 1, "I組 首名", "待定(小組第三)"), ("K", 1, "K組 首名", "L", 1, "L組 首名")
    ]
    for i, cfg in enumerate(mock_r32):
        if len(cfg) == 4:
            g_h, p_h, mock_h, mock_a = cfg
            h = get_group_team(standings_data, g_h, p_h, mock_h)
            a = mock_a
        else:
            g_h, p_h, mock_h, g_a, p_a, mock_a = cfg
            h = get_group_team(standings_data, g_h, p_h, mock_h)
            a = get_group_team(standings_data, g_a, p_a, mock_a)
        mock_matches.append({"stage": "LAST_32", "status": "SCHEDULED", "utcDate": get_mock_date("LAST_32", i), "homeTeam": {"name": h}, "awayTeam": {"name": a}, "score": {"fullTime": {"home": None, "away": None}}})
    
    for i in range(8): mock_matches.append({"stage": "LAST_16", "status": "SCHEDULED", "utcDate": get_mock_date("LAST_16", i), "homeTeam": {"name": "32強勝者"}, "awayTeam": {"name": "32強勝者"}, "score": {"fullTime": {"home": None, "away": None}}})
    for i in range(4): mock_matches.append({"stage": "QUARTER_FINALS", "status": "SCHEDULED", "utcDate": get_mock_date("QUARTER_FINALS", i), "homeTeam": {"name": "16強勝者"}, "awayTeam": {"name": "16強勝者"}, "score": {"fullTime": {"home": None, "away": None}}})
    for i in range(2): mock_matches.append({"stage": "SEMI_FINALS", "status": "SCHEDULED", "utcDate": get_mock_date("SEMI_FINALS", i), "homeTeam": {"name": "8強勝者"}, "awayTeam": {"name": "8強勝者"}, "score": {"fullTime": {"home": None, "away": None}}})
    mock_matches.append({"stage": "FINAL", "status": "SCHEDULED", "utcDate": get_mock_date("FINAL", 0), "homeTeam": {"name": "準決賽勝者"}, "awayTeam": {"name": "準決賽勝者"}, "score": {"fullTime": {"home": None, "away": None}}})
    mock_matches.append({"stage": "THIRD_PLACE", "status": "SCHEDULED", "utcDate": get_mock_date("THIRD_PLACE", 0), "homeTeam": {"name": "準決賽敗者"}, "awayTeam": {"name": "準決賽敗者"}, "score": {"fullTime": {"home": None, "away": None}}})
    return mock_matches

def get_padded_matches(matches, stage, expected_count):
    stage_matches = [m for m in matches if m.get("stage") == stage]
    # 【關鍵修正】: 避免以時間打亂對立組合
    stage_matches.sort(key=lambda x: x.get("id", 0))
    while len(stage_matches) < expected_count:
        idx = len(stage_matches)
        stage_matches.append({
            "stage": stage,
            "status": "SCHEDULED",
            "utcDate": get_mock_date(stage, idx),
            "homeTeam": {"name": "待定"}, 
            "awayTeam": {"name": "待定"}
        })
    return stage_matches[:expected_count]

# ==========================================
# 3. UI 模組：圖片國旗支援與 HTML 卡片重構
# ==========================================
def get_flag_url(team_en):
    code = TEAM_FLAG_CODE.get(team_en.strip())
    return f"https://flagcdn.com/24x18/{code}.png" if code else None

def get_flag_html(team_en, height=14):
    url = get_flag_url(team_en)
    if url:
        return f'<img src="{url}" style="height:{height}px; width:auto; vertical-align:middle; margin-right:4px; border-radius:2px; box-shadow:0 0 1px rgba(0,0,0,0.3);">'
    return ""

def get_svg_connector(count, h):
    """繪製連接線"""
    svg_h = 2 * h
    y1 = h / 2
    y2 = y1 + h
    y_mid = h
    res = '<div style="display:flex;flex-direction:column;width:30px;">'
    for _ in range(count):
        res += f'<div style="height:{svg_h}px;display:flex;align-items:center;justify-content:center;"><svg width="30" height="{svg_h}" style="display:block;"><path d="M 0 {y1} L 15 {y1} L 15 {y2} L 0 {y2} M 15 {y_mid} L 30 {y_mid}" stroke="#bdc1c6" stroke-width="2" fill="transparent" stroke-linecap="square"/></svg></div>'
    res += '</div>'
    return res

def get_match_card_html(match):
    home_en = match.get("homeTeam", {}).get("name") or "TBD"
    away_en = match.get("awayTeam", {}).get("name") or "TBD"
    home = TEAM_TRANSLATION.get(home_en.strip(), home_en)
    away = TEAM_TRANSLATION.get(away_en.strip(), away_en)

    h_rank = TEAM_RANKING.get(home_en.strip(), "") if is_real_team(home_en) else ""
    a_rank = TEAM_RANKING.get(away_en.strip(), "") if is_real_team(away_en) else ""
    
    h_flag = get_flag_html(home_en, height=12) if is_real_team(home_en) else ""
    a_flag = get_flag_html(away_en, height=12) if is_real_team(away_en) else ""
    
    h_display = f"{h_flag}{home} <span style='color:#9aa0a6;font-size:11px;margin-left:4px;'>#{h_rank}</span>" if h_rank else f"{h_flag}{home}"
    a_display = f"{a_flag}{away} <span style='color:#9aa0a6;font-size:11px;margin-left:4px;'>#{a_rank}</span>" if a_rank else f"{a_flag}{away}"

    score_obj = match.get("score", {}) or {}
    full_time = score_obj.get("fullTime", {}) or {}
    h_score = full_time.get("home") if full_time.get("home") is not None else "-"
    a_score = full_time.get("away") if full_time.get("away") is not None else "-"

    tpe_dt = get_taipei_time(match.get("utcDate", ""))
    dt_display = tpe_dt.strftime("%m/%d %H:%M") if tpe_dt else "時間待定"

    html = f'<div style="background-color:#ffffff;border:1px solid #dadce0;border-radius:8px;padding:6px 10px;width:170px;height:82px;box-sizing:border-box;font-family:sans-serif;box-shadow:0 1px 2px rgba(0,0,0,0.05);z-index:10;display:flex;flex-direction:column;justify-content:space-between;"><div style="font-size:11px;line-height:1.2;color:#70757a;border-bottom:1px solid #f1f3f4;padding-bottom:3px;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{dt_display}</div><div style="display:flex;justify-content:space-between;align-items:center;flex:1;"><span style="font-size:13px;line-height:1.2;font-weight:500;color:#202124;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;min-width:0;">{h_display}</span><span style="font-size:13px;line-height:1.2;font-weight:bold;color:#202124;margin-left:4px;">{h_score}</span></div><div style="display:flex;justify-content:space-between;align-items:center;flex:1;"><span style="font-size:13px;line-height:1.2;font-weight:500;color:#202124;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;min-width:0;">{a_display}</span><span style="font-size:13px;line-height:1.2;font-weight:bold;color:#202124;margin-left:4px;">{a_score}</span></div></div>'
    return html

def build_col(matches, cell_height):
    res = '<div style="display:flex;flex-direction:column;width:170px;">'
    for m in matches:
        res += f'<div style="height:{cell_height}px;display:flex;align-items:center;justify-content:center;">{get_match_card_html(m)}</div>'
    res += '</div>'
    return res

def display_match_item(match):
    """採用 Flexbox 的客製化精緻賽程卡，取代 st.metric，解決排版與字體國旗問題"""
    home_en = match.get("homeTeam", {}).get("name") or "TBD"
    away_en = match.get("awayTeam", {}).get("name") or "TBD"
    home = TEAM_TRANSLATION.get(home_en.strip(), home_en)
    away = TEAM_TRANSLATION.get(away_en.strip(), away_en)
    
    h_rank = TEAM_RANKING.get(home_en.strip(), "") if is_real_team(home_en) else ""
    a_rank = TEAM_RANKING.get(away_en.strip(), "") if is_real_team(away_en) else ""
    h_flag = get_flag_html(home_en, height=16) if is_real_team(home_en) else ""
    a_flag = get_flag_html(away_en, height=16) if is_real_team(away_en) else ""
    
    h_rank_str = f" <span style='font-size:12px; font-weight:normal; color:#9aa0a6;'>#{h_rank}</span>" if h_rank else ""
    a_rank_str = f" <span style='font-size:12px; font-weight:normal; color:#9aa0a6;'>#{a_rank}</span>" if a_rank else ""
    
    score_obj = match.get("score", {}) or {}
    full_time = score_obj.get("fullTime", {}) or {}
    h_score = full_time.get("home") if full_time.get("home") is not None else "-"
    a_score = full_time.get("away") if full_time.get("away") is not None else "-"
    
    status_raw = match.get("status", "UNKNOWN")
    status_text = STATUS_MAP.get(status_raw, status_raw)
    tpe_dt = get_taipei_time(match.get("utcDate", ""))
    
    time_display = tpe_dt.strftime("%H:%M") if tpe_dt else "時間待定"
    
    card_html = f"""
    <div style="display:flex; justify-content:space-between; align-items:center; background:#ffffff; padding:12px 10px; border-radius:8px; margin-bottom:12px; border:1px solid #eaebed; box-shadow:0 1px 2px rgba(0,0,0,0.05); font-family:sans-serif;">
        <div style="flex:1; text-align:center; min-width:0;">
            <div style="font-size:14px; font-weight:bold; color:#202124; margin-bottom:4px; display:flex; justify-content:center; align-items:center; flex-wrap:wrap;">
                {h_flag}<span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{home}</span>{h_rank_str}
            </div>
            <div style="font-size:26px; font-weight:bold; color:#202124;">{h_score}</div>
        </div>
        <div style="width:85px; text-align:center; border-left:1px solid #f1f3f4; border-right:1px solid #f1f3f4; padding:0 5px; flex-shrink:0;">
            <div style="font-size:12px; color:#70757a; margin-bottom:6px; white-space:nowrap;">{time_display} 開踢</div>
            <div style="font-size:13px; font-weight:bold; color:#1a73e8; background:#e8f0fe; padding:3px 6px; border-radius:4px; display:inline-block; white-space:nowrap;">{status_text}</div>
        </div>
        <div style="flex:1; text-align:center; min-width:0;">
            <div style="font-size:14px; font-weight:bold; color:#202124; margin-bottom:4px; display:flex; justify-content:center; align-items:center; flex-wrap:wrap;">
                {a_flag}<span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{away}</span>{a_rank_str}
            </div>
            <div style="font-size:26px; font-weight:bold; color:#202124;">{a_score}</div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

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
        
    for stage_code in ko_stages:
        s_matches = [m for m in all_m if m.get("stage") == stage_code]
        # 【關鍵修正】: 取消以時間排序，確保賽事維持晉級路線對位
        s_matches.sort(key=lambda x: x.get("id", 0))
        for i, m in enumerate(s_matches):
            if not m.get("utcDate"):
                m["utcDate"] = get_mock_date(stage_code, i)

with sub_tab1:
    st.subheader("🌳 淘汰賽晉級樹狀圖 (依據結構排列配對)")
    
    r1_m = get_padded_matches(all_m, "LAST_32", 16)
    r2_m = get_padded_matches(all_m, "LAST_16", 8)
    r3_m = get_padded_matches(all_m, "QUARTER_FINALS", 4)
    r4_m = get_padded_matches(all_m, "SEMI_FINALS", 2)
    r5_f = get_padded_matches(all_m, "FINAL", 1)[0]
    r5_t = get_padded_matches(all_m, "THIRD_PLACE", 1)[0]

    r1_html = build_col(r1_m, 90)
    r2_html = build_col(r2_m, 180)
    r3_html = build_col(r3_m, 360)
    r4_html = build_col(r4_m, 720)
            
    r5_html = f'<div style="display:flex;flex-direction:column;width:170px;position:relative;"><div style="height:1440px;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100%;"><div style="font-size:12px;color:#ea4335;font-weight:bold;margin-bottom:4px;">🏆 冠軍戰</div>{get_match_card_html(r5_f)}</div><div style="position:absolute;top:850px;left:0;width:100%;display:flex;flex-direction:column;align-items:center;"><div style="font-size:12px;color:#5f6368;font-weight:bold;margin-bottom:4px;">🥉 季軍戰</div>{get_match_card_html(r5_t)}</div></div>'
    
    header_html = '<div style="display:flex;min-width:1000px;margin-bottom:12px;"><div style="width:170px;text-align:center;font-weight:bold;color:#5f6368;font-size:14px;">32強賽</div><div style="width:30px;"></div><div style="width:170px;text-align:center;font-weight:bold;color:#5f6368;font-size:14px;">16強賽</div><div style="width:30px;"></div><div style="width:170px;text-align:center;font-weight:bold;color:#5f6368;font-size:14px;">8強賽</div><div style="width:30px;"></div><div style="width:170px;text-align:center;font-weight:bold;color:#5f6368;font-size:14px;">4強賽</div><div style="width:30px;"></div><div style="width:170px;text-align:center;font-weight:bold;color:#ea4335;font-size:14px;">決賽階段</div></div>'
    
    # 重新帶入 get_svg_connector 將結構重新連線
    bracket_container = f'<div style="display:flex;min-width:1000px;height:1440px;">{r1_html}{get_svg_connector(8, 90)}{r2_html}{get_svg_connector(4, 180)}{r3_html}{get_svg_connector(2, 360)}{r4_html}{get_svg_connector(1, 720)}{r5_html}</div>'

    bracket_html = f'<div style="overflow-x:auto;background-color:#f8f9fa;padding:20px;border-radius:12px;border:1px solid #eaebed;margin-top:10px;">{header_html}{bracket_container}</div>'
    
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
                flag_url = get_flag_url(team_en) if is_real_team(team_en) else None
                
                table_rows.append({
                    "排名": entry.get("position"), "國旗": flag_url, "球隊": team_zh, "已賽": entry.get("playedGames"),
                    "勝": entry.get("won"), "和": entry.get("draw"), "敗": entry.get("lost"),
                    "進/失球": f"{entry.get('goalsFor')} / {entry.get('goalsAgainst')}",
                    "淨勝球(GD)": entry.get("goalDifference"), "總積分": entry.get("points")
                })
            st.dataframe(
                table_rows, 
                use_container_width=True, 
                hide_index=True,
                column_config={"國旗": st.column_config.ImageColumn("國旗", help="國家國旗")}
            )
