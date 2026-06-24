import streamlit as st
import requests
from datetime import datetime, timedelta

# ==========================================
# 1. API 設定區與內部資料庫
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

STATUS_MAP = {
    "FINISHED": "比賽結束", "IN_PLAY": "進行中", "PAUSED": "中場休息",
    "TIMED": "未開始", "SCHEDULED": "預定賽程", "POSTPONED": "延期"
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

# 判斷是否為真實的國家隊伍（避開官方的 TBD、Winner 等暫定詞彙）
def is_real_team(team_name):
    if not team_name: return False
    fake_keywords = ["TBD", "待定", "WINNER", "LOSER", "GROUP", "晉級", "首名", "次名", "勝者", "敗者", "UNKNOWN"]
    name_upper = str(team_name).upper()
    return not any(kw in name_upper for kw in fake_keywords)

# ==========================================
# 2. 自動連網抓取與智慧預填機制 (核心更新區)
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
        return {"error": f"國際伺服器積分回應錯誤 (代碼 {response.status_code})"}
    except Exception as e:
        return {"error": f"積分連線異常：{e}"}

def get_taipei_time(utc_date_str):
    try:
        utc_dt = datetime.strptime(utc_date_str, "%Y-%m-%dT%H:%M:%SZ")
        return utc_dt + timedelta(hours=8)
    except:
        return None

# ✨ 即時從「積分榜」抓取當前小組第一、第二名，達成 B組完賽立刻連動
def get_group_team(standings_data, group_letter, pos, fallback):
    if not standings_data: return fallback
    for g in standings_data:
        if g.get("group") == f"GROUP_{group_letter}":
            table = g.get("table", [])
            if len(table) >= pos:
                t_name = table[pos-1].get("team", {}).get("name", "")
                if t_name: return t_name # 回傳英文原名，後續流程會自動翻譯與掛上排名
    return fallback

# ✨ 保留 API 的時間與數據，只將「TBD」置換為我們的智慧名單
def inject_live_knockout_teams(all_matches, standings_data):
    mock_r32 = [
        (get_group_team(standings_data, 'A', 1, "A組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'B', 2, "B組 次名"), get_group_team(standings_data, 'C', 2, "C組 次名")),
        (get_group_team(standings_data, 'D', 1, "D組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'E', 2, "E組 次名"), get_group_team(standings_data, 'F', 2, "F組 次名")),
        (get_group_team(standings_data, 'G', 1, "G組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'H', 2, "H組 次名"), get_group_team(standings_data, 'I', 2, "I組 次名")),
        (get_group_team(standings_data, 'J', 1, "J組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'K', 2, "K組 次名"), get_group_team(standings_data, 'L', 2, "L組 次名")),
        (get_group_team(standings_data, 'B', 1, "B組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'A', 2, "A組 次名"), get_group_team(standings_data, 'D', 2, "D組 次名")),
        (get_group_team(standings_data, 'C', 1, "C組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'E', 1, "E組 首名"), get_group_team(standings_data, 'H', 1, "H組 首名")),
        (get_group_team(standings_data, 'F', 1, "F組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'G', 2, "G組 次名"), get_group_team(standings_data, 'J', 2, "J組 次名")),
        (get_group_team(standings_data, 'I', 1, "I組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'K', 1, "K組 首名"), get_group_team(standings_data, 'L', 1, "L組 首名"))
    ]
    r32_count = 0
    for m in all_matches:
        stage = m.get("stage")
        if stage in ["LAST_32", "LAST_16", "QUARTER_FINALS", "SEMI_FINALS", "FINAL", "THIRD_PLACE"]:
            home_team = m.get("homeTeam", {}).get("name") if m.get("homeTeam") else None
            away_team = m.get("awayTeam", {}).get("name") if m.get("awayTeam") else None
            
            if stage == "LAST_32":
                mock_h, mock_a = mock_r32[r32_count % 16]
                if not is_real_team(home_team):
                    if "homeTeam" not in m or m["homeTeam"] is None: m["homeTeam"] = {}
                    m["homeTeam"]["name"] = mock_h
                if not is_real_team(away_team):
                    if "awayTeam" not in m or m["awayTeam"] is None: m["awayTeam"] = {}
                    m["awayTeam"]["name"] = mock_a
                r32_count += 1
            else:
                fallback_map = {"LAST_16": "32強晉級隊", "QUARTER_FINALS": "16強晉級隊", "SEMI_FINALS": "8強晉級隊", "FINAL": "準決賽勝者", "THIRD_PLACE": "準決賽敗者"}
                mock_val = fallback_map.get(stage, "待定")
                if not is_real_team(home_team):
                    if "homeTeam" not in m or m["homeTeam"] is None: m["homeTeam"] = {}
                    m["homeTeam"]["name"] = mock_val
                if not is_real_team(away_team):
                    if "awayTeam" not in m or m["awayTeam"] is None: m["awayTeam"] = {}
                    m["awayTeam"]["name"] = mock_val

def get_mock_knockout_matches(standings_data):
    mock_matches = []
    # 如果 API 完全空白，才執行全新建構（這通常只在開賽前發生）
    # 這裡的邏輯與上方完全一致，確保 fallback 有效
    mock_r32 = [
        (get_group_team(standings_data, 'A', 1, "A組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'B', 2, "B組 次名"), get_group_team(standings_data, 'C', 2, "C組 次名")),
        (get_group_team(standings_data, 'D', 1, "D組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'E', 2, "E組 次名"), get_group_team(standings_data, 'F', 2, "F組 次名")),
        (get_group_team(standings_data, 'G', 1, "G組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'H', 2, "H組 次名"), get_group_team(standings_data, 'I', 2, "I組 次名")),
        (get_group_team(standings_data, 'J', 1, "J組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'K', 2, "K組 次名"), get_group_team(standings_data, 'L', 2, "L組 次名")),
        (get_group_team(standings_data, 'B', 1, "B組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'A', 2, "A組 次名"), get_group_team(standings_data, 'D', 2, "D組 次名")),
        (get_group_team(standings_data, 'C', 1, "C組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'E', 1, "E組 首名"), get_group_team(standings_data, 'H', 1, "H組 首名")),
        (get_group_team(standings_data, 'F', 1, "F組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'G', 2, "G組 次名"), get_group_team(standings_data, 'J', 2, "J組 次名")),
        (get_group_team(standings_data, 'I', 1, "I組 首名"), "待定 (小組第三)"), 
        (get_group_team(standings_data, 'K', 1, "K組 首名"), get_group_team(standings_data, 'L', 1, "L組 首名"))
    ]
    for h, a in mock_r32:
        mock_matches.append({"stage": "LAST_32", "status": "SCHEDULED", "utcDate": "", "homeTeam": {"name": h}, "awayTeam": {"name": a}, "score": {"fullTime": {"home": "-", "away": "-"}}})
    for _ in range(8):
        mock_matches.append({"stage": "LAST_16", "status": "SCHEDULED", "utcDate": "", "homeTeam": {"name": "32強晉級隊"}, "awayTeam": {"name": "32強晉級隊"}, "score": {"fullTime": {"home": "-", "away": "-"}}})
    for _ in range(4):
        mock_matches.append({"stage": "QUARTER_FINALS", "status": "SCHEDULED", "utcDate": "", "homeTeam": {"name": "16強晉級隊"}, "awayTeam": {"name": "16強晉級隊"}, "score": {"fullTime": {"home": "-", "away": "-"}}})
    for _ in range(2):
        mock_matches.append({"stage": "SEMI_FINALS", "status": "SCHEDULED", "utcDate": "", "homeTeam": {"name": "8強晉級隊"}, "awayTeam": {"name": "8強晉級隊"}, "score": {"fullTime": {"home": "-", "away": "-"}}})
    mock_matches.append({"stage": "FINAL", "status": "SCHEDULED", "utcDate": "", "homeTeam": {"name": "準決賽勝者"}, "awayTeam": {"name": "準決賽勝者"}, "score": {"fullTime": {"home": "-", "away": "-"}}})
    mock_matches.append({"stage": "THIRD_PLACE", "status": "SCHEDULED", "utcDate": "", "homeTeam": {"name": "準決賽敗者"}, "awayTeam": {"name": "準決賽敗者"}, "score": {"fullTime": {"home": "-", "away": "-"}}})
    return mock_matches

# ==========================================
# 3. UI 模組：對戰確認視覺標籤
# ==========================================
def get_match_card_html(match):
    home_en = match.get("homeTeam", {}).get("name") or "TBD"
    away_en = match.get("awayTeam", {}).get("name") or "TBD"
    home = TEAM_TRANSLATION.get(home_en.strip(), home_en)
    away = TEAM_TRANSLATION.get(away_en.strip(), away_en)
    
    home_rank = TEAM_RANKING.get(home_en.strip(), "-")
    away_rank = TEAM_RANKING.get(away_en.strip(), "-")
    h_rank_str = f" <span style='font-size:10px; color:#9E9E9E;'>#{home_rank}</span>" if home_rank != "-" else ""
    a_rank_str = f" <span style='font-size:10px; color:#9E9E9E;'>#{away_rank}</span>" if away_rank != "-" else ""

    score_obj = match.get("score", {}) or {}
    full_time = score_obj.get("fullTime", {}) or {}
    h_score = full_time.get("home") if full_time.get("home") is not None else "-"
    a_score = full_time.get("away") if full_time.get("away") is not None else "-"

    status_raw = match.get("status", "UNKNOWN")
    status_text = STATUS_MAP.get(status_raw, status_raw)
    
    tpe_dt = get_taipei_time(match.get("utcDate", ""))
    # ✨ 修正：如果沒有時間，顯示「時間待定」，若有時間則完美顯示
    dt_display = tpe_dt.strftime("%m/%d %H:%M") if tpe_dt else "時間待定"
    status_color = "#E53935" if status_raw in ["IN_PLAY", "PAUSED"] else "#757575"

    is_confirmed = is_real_team(home_en) and is_real_team(away_en)
    badge_html = " <span style='color: #43A047;'>✅已確認</span>" if is_confirmed and status_raw in ["TIMED", "SCHEDULED"] else ""
    if not is_confirmed and status_raw in ["TIMED", "SCHEDULED"]:
        badge_html = " <span style='color: #FB8C00;'>⏳對手待定</span>"

    html = (
        f'<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; margin-bottom: 12px; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-width: 170px;">'
        f'<div style="font-size: 11px; color: {status_color}; text-align: center; margin-bottom: 8px; font-weight: bold;">{dt_display} | {status_text}{badge_html}</div>'
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">'
        f'<span style="font-size: 14px; font-weight: 600; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 110px;">{home}{h_rank_str}</span>'
        f'<span style="font-size: 15px; font-weight: 900; color: #1E88E5;">{h_score}</span>'
        f'</div>'
        f'<div style="display: flex; justify-content: space-between; align-items: center;">'
        f'<span style="font-size: 14px; font-weight: 600; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 110px;">{away}{a_rank_str}</span>'
        f'<span style="font-size: 15px; font-weight: 900; color: #1E88E5;">{a_score}</span>'
        f'</div>'
        f'</div>'
    )
    return html

def display_match_item(match, display_date=True):
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
    h_score = full_time.get("home") if full_time.get("home") is not None else "-"
    a_score = full_time.get("away") if full_time.get("away") is not None else "-"
    status_raw = match.get("status", "UNKNOWN")
    status_text = STATUS_MAP.get(status_raw, status_raw)
    tpe_dt = get_taipei_time(match.get("utcDate", ""))
    
    is_confirmed = is_real_team(home_en) and is_real_team(away_en)
    badge = " <span style='font-size: 14px; background-color: #E8F5E9; color: #2E7D32; padding: 2px 6px; border-radius: 4px; margin-left: 10px;'>✅ 最新確認組合</span>" if is_confirmed and status_raw in ["TIMED", "SCHEDULED"] else ""
    
    st.markdown("---")
    # ✨ 修正：確保如果有 utcDate，列表模式也能印出準確時間
    if display_date:
        dt_display = tpe_dt.strftime("%m/%d %H:%M") if tpe_dt else "時間待定"
        st.markdown(f"### 🏟️ {home}{h_rank_tag} 🆚 {away}{a_rank_tag}{badge} <span style='font-size: 14px; color: gray; margin-left: 10px;'>({dt_display})</span>", unsafe_allow_html=True)
    else:
        time_str = tpe_dt.strftime("%H:%M") if tpe_dt else "時間待定"
        st.markdown(f"### 🏟️ {home}{h_rank_tag} 🆚 {away}{a_rank_tag}{badge} <span style='font-size: 14px; color: gray; margin-left: 10px;'>({time_str} 開踢)</span>", unsafe_allow_html=True)

    h_display = 0 if h_score == "-" else h_score
    a_display = 0 if a_score == "-" else a_score
    col1, col2, col3 = st.columns(3)
    col1.metric(label=home, value=h_display)
    col2.metric(label="賽事狀態", value=status_text)
    col3.metric(label=away, value=a_display)
    
    with st.expander("📊 查看賽後攻防統計與進球名單"):
        ht = score_obj.get('halfTime', {}) or {}
        et = score_obj.get('extraTime', {}) or {}
        pk = score_obj.get('penalties', {}) or {}
        
        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("半場比分", f"{ht.get('home', '-')} : {ht.get('away', '-')}")
        sc2.metric("延長賽", f"{et.get('home', '-')} : {et.get('away', '-')}" if et.get('home') is not None else "無")
        sc3.metric("PK 戰", f"{pk.get('home', '-')} : {pk.get('away', '-')}" if pk.get('home') is not None else "無")
        
        st.markdown("---")
        goals = match.get("goals", [])
        st.markdown("**⚽ 進攻紀錄 (進球者)**")
        if goals:
            for g in goals:
                scorer = g.get("scorer", {}).get("name", "Unknown")
                minute = g.get("minute", "")
                team_name_en = g.get("team", {}).get("name", "")
                team_zh = TEAM_TRANSLATION.get(team_name_en.strip(), team_name_en)
                st.caption(f"⏱️ {minute}' - {scorer} ({team_zh})")
        else:
            st.caption("尚無進球紀錄。")

        st.markdown("**📈 進階攻防數據**")
        stats = match.get("statistics")
        if stats:
            st.json(stats)
        else:
            st.info("💡 官方免費版 API 預設不提供批量控球率、射門次數等數據。")

# ==========================================
# 4. 主程式排版
# ==========================================
st.set_page_config(page_title="2026世足動態全功能看板", page_icon="🏆", layout="wide")

st.title("🏆 2026 世足賽動態看板")
st.markdown("美加墨聯合主辦｜賽程・即時比分・分組積分・晉級樹狀圖全自動同步")

if st.button("🔄 立即刷新、同步最新數據", use_container_width=True):
    st.cache_data.clear()

matches_result = fetch_all_matches()
standings_result = fetch_standings()

if "error" in matches_result:
    st.error(f"❌ 賽程載入失敗：{matches_result['error']}")
else:
    all_matches = matches_result.get("data", [])
    standings_data = standings_result.get("data", []) if "error" not in standings_result else []
    
    ko_stages = ["LAST_32", "LAST_16", "QUARTER_FINALS", "SEMI_FINALS", "THIRD_PLACE", "FINAL"]
    ko_matches = [m for m in all_matches if m.get("stage") in ko_stages]
    
    # ✨ 核心修正：不再直接抹除 API 資料，而是去填補 API 裡空缺的 TBD
    if not ko_matches:
        all_matches.extend(get_mock_knockout_matches(standings_data))
    else:
        inject_live_knockout_teams(all_matches, standings_data)
        
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 淘汰賽列表", "🌳 晉級樹狀圖", "⚽ 分組賽進度", "📊 各組積分表", "📡 今日與次日焦點"])
    
    with tab1:
        st.subheader("世界盃淘汰賽最新戰況 (列表模式)")
        ko_matches_updated = [m for m in all_matches if m.get("stage") in ko_stages]
        for stage_code in reversed(ko_stages):
            stage_matches = [m for m in ko_matches_updated if m.get("stage") == stage_code]
            if stage_matches:
                with st.expander(STAGE_MAP.get(stage_code, stage_code)):
                    for m in stage_matches:
                        display_match_item(m, display_date=True)

    with tab2:
        st.subheader("🌳 淘汰賽晉級樹狀圖 (Bracket)")
        st.caption("💡 提示：在手機上可 **左右滑動** 檢視完整樹狀圖。只要分組賽一結束，晉級名單會 **自動連動取代** 預定位置！")
        tree_stages = ["LAST_32", "LAST_16", "QUARTER_FINALS", "SEMI_FINALS", "FINAL", "THIRD_PLACE"]
        tree_matches = [m for m in all_matches if m.get("stage") in tree_stages]
        
        col_html = {"LAST_32": "", "LAST_16": "", "QUARTER_FINALS": "", "SEMI_FINALS": "", "FINAL": "", "THIRD_PLACE": ""}
        for m in tree_matches:
            stage = m.get("stage")
            if stage in col_html:
                col_html[stage] += get_match_card_html(m)
                
        bracket_html = (
            '<div style="overflow-x: auto; padding-bottom: 20px; background-color: #f0f2f6; padding: 20px; border-radius: 12px; margin-top: 10px;">'
            '<div style="display: flex; min-width: 1000px; gap: 15px;">'
            '<div style="flex: 1;"><h4 style="text-align: center; color: #424242; font-size: 16px; margin-bottom:15px;">🚀 32強賽</h4>' + col_html["LAST_32"] + '</div>'
            '<div style="flex: 1;"><h4 style="text-align: center; color: #424242; font-size: 16px; margin-bottom:15px;">🎯 16強賽</h4>' + col_html["LAST_16"] + '</div>'
            '<div style="flex: 1;"><h4 style="text-align: center; color: #424242; font-size: 16px; margin-bottom:15px;">⚔️ 8強賽</h4>' + col_html["QUARTER_FINALS"] + '</div>'
            '<div style="flex: 1;"><h4 style="text-align: center; color: #424242; font-size: 16px; margin-bottom:15px;">⭐ 4強賽</h4>' + col_html["SEMI_FINALS"] + '</div>'
            '<div style="flex: 1;"><h4 style="text-align: center; color: #FF8F00; font-size: 16px; margin-bottom:15px;">🏆 冠軍戰</h4>' + col_html["FINAL"] +
            '<h4 style="text-align: center; color: #8D6E63; margin-top: 30px; font-size: 16px; margin-bottom:15px;">🥉 季軍戰</h4>' + col_html["THIRD_PLACE"] + '</div>'
            '</div></div>'
        )
        st.markdown(bracket_html, unsafe_allow_html=True)

    with tab3:
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
                        display_match_item(m, display_date=True)

    with tab4:
        st.subheader("2026 世界盃小組積分榜")
        if "error" in standings_result:
            st.error(f"❌ 積分表同步失敗：{standings_result['error']}")
        else:
            standings_data_table = standings_result.get("data", [])
            if not standings_data_table:
                st.info("⚽ 官方尚未上傳分組積分表數據。")
            else:
                for group_data in standings_data_table:
                    g_code = group_data.get("group")
                    g_name = GROUP_MAP.get(g_code, g_code)
                    
                    st.write(f"#### 📍 {g_name}")
                    table_rows = []
                    for entry in group_data.get("table", []):
                        team_en = entry.get("team", {}).get("name") or "TBD"
                        team_zh = TEAM_TRANSLATION.get(team_en.strip(), team_en)
                        team_rank = TEAM_RANKING.get(team_en.strip(), "-")
                        
                        table_rows.append({
                            "排名": entry.get("position"), 
                            "球隊": team_zh, 
                            "世界排名": team_rank,
                            "已賽": entry.get("playedGames"),
                            "勝": entry.get("won"), "和": entry.get("draw"), "敗": entry.get("lost"),
                            "進/失球": f"{entry.get('goalsFor')}/{entry.get('goalsAgainst')}",
                            "得失差": entry.get("goalDifference"), "積分": entry.get("points")
                        })
                    st.dataframe(table_rows, use_container_width=True, hide_index=True)

    with tab5:
        today_tpe_date = (datetime.utcnow() + timedelta(hours=8)).date()
        tomorrow_tpe_date = today_tpe_date + timedelta(days=1)
        
        today_matches = []
        tomorrow_matches = []
        for m in all_matches:
            m_tpe_dt = get_taipei_time(m.get("utcDate", ""))
            if m_tpe_dt:
                if m_tpe_dt.date() == today_tpe_date:
                    today_matches.append(m)
                elif m_tpe_dt.date() == tomorrow_tpe_date:
                    tomorrow_matches.append(m)
        
        st.subheader(f"🔥 今日焦點賽事 ({today_tpe_date.strftime('%m/%d')})")
        if not today_matches:
            st.info("⚽ 今日暫無賽事。")
        else:
            for match in today_matches:
                display_match_item(match, display_date=False)
                
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.subheader(f"🔜 明日賽程預告 ({tomorrow_tpe_date.strftime('%m/%d')})")
        if not tomorrow_matches:
            st.info("⚽ 明日暫無賽事安排。")
        else:
            for match in tomorrow_matches:
                display_match_item(match, display_date=False)
