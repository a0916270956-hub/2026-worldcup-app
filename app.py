import streamlit as st
import requests
from datetime import datetime

# ==========================================
# 1. API 設定區
# ==========================================
API_TOKEN = "d5921a999fd5418aa3c5026db3889cf2"

# 全球球隊中英文名稱翻譯字典 (確保動態抓取時畫面上顯示流暢中文)
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

# 賽事狀態中文化
STATUS_MAP = {
    "FINISHED": "比賽結束", "IN_PLAY": "進行中", "PAUSED": "中場休息",
    "TIMED": "未開始", "SCHEDULED": "已排程", "POSTPONED": "延期"
}

# 賽段中文化
STAGE_MAP = {
    "FINAL": "🏆 冠軍總決賽",
    "THIRD_PLACE": "🥉 季軍爭奪戰",
    "SEMI_FINALS": "⭐ 4強準決賽",
    "QUARTER_FINALS": "⚔️ 8強半決賽",
    "LAST_16": "🎯 16強淘汰賽",
    "LAST_32": "🚀 32強淘汰賽",
    "GROUP_STAGE": "⚽ 分組賽段"
}

# 組別中文化
GROUP_MAP = {
    "GROUP_A": "A組", "GROUP_B": "B組", "GROUP_C": "C組", "GROUP_D": "D組",
    "GROUP_E": "E組", "GROUP_F": "F組", "GROUP_G": "G組", "GROUP_H": "H組",
    "GROUP_I": "I組", "GROUP_J": "J組", "GROUP_K": "K組", "GROUP_L": "L組"
}

# ==========================================
# 2. 自動連網抓取函式 (Football-Data.org 專用)
# ==========================================
@st.cache_data(ttl=60)
def fetch_all_matches(season="2026"):
    url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": API_TOKEN}
    params = {"season": season}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return {"data": response.json().get("matches", [])}
        elif response.status_code == 429:
            return {"error": "已達到每分鐘請求次數限制，請等候一分鐘後再刷新。"}
        else:
            return {"error": f"國際伺服器回應錯誤 (代碼 {response.status_code})"}
    except Exception as e:
        return {"error": f"系統連線異常：{e}"}

# ==========================================
# 3. 賽程卡片渲染輔助功能
# ==========================================
def display_match_item(match):
    home_en = match.get("homeTeam", {}).get("name", "Unknown")
    away_en = match.get("awayTeam", {}).get("name", "Unknown")
    home = TEAM_TRANSLATION.get(home_en, home_en)
    away = TEAM_TRANSLATION.get(away_en, away_en)
    
    score_data = match.get("score", {}).get("fullTime", {})
    h_score = score_data.get("home")
    a_score = score_data.get("away")
    
    status_raw = match.get("status", "UNKNOWN")
    status_text = STATUS_MAP.get(status_raw, status_raw)
    
    # 格式化顯示時間
    utc_date = match.get("utcDate", "")
    try:
        dt_display = utc_date.replace("T", " ").replace("Z", "")[:16]
    except:
        dt_display = utc_date

    if h_score is not None and a_score is not None:
        score_display = f"【{h_score} : {a_score}】 ({status_text})"
    else:
        score_display = f"【尚未開賽】 (預計時間: {dt_display})"
        
    st.markdown(f"🕒 {dt_display} &nbsp;&nbsp; **{home} VS {away}** &nbsp;&nbsp; `{score_display}`")

# ==========================================
# 4. 主程式介面與排版
# ==========================================
st.set_page_config(page_title="2026世足全自動動態看板", page_icon="🏆", layout="centered")

st.title("🏆 2026 世足賽程與即時比分")
st.markdown("美加墨聯合主辦｜動態比分全自動同步系統")

if st.button("🔄 立即刷新、同步最新戰況", use_container_width=True):
    st.cache_data.clear()

mode = st.radio("資料庫模式：", ["正式模式 (2026真實賽況)", "測試模式 (2022歷史回顧)"], horizontal=True)
target_season = "2022" if "2022" in mode else "2026"

result = fetch_all_matches(season=target_season)

if "error" in result:
    st.error(f"❌ {result['error']}")
else:
    all_matches = result.get("data", [])
    
    tab1, tab2, tab3 = st.tabs(["🏆 淘汰賽戰況", "⚽ 分組賽進度", "📡 今日即時焦點"])
    
    # 【分頁1：淘汰賽 (動態刷新)】
    with tab1:
        st.subheader("世界盃淘汰賽最新戰況")
        ko_stages = ["LAST_32", "LAST_16", "QUARTER_FINALS", "SEMI_FINALS", "THIRD_PLACE", "FINAL"]
        ko_matches = [m for m in all_matches if m.get("stage") in ko_stages]
        
        if not ko_matches:
            st.info("⚽ 淘汰賽組合將於分組賽結束後自動生成。")
        else:
            for stage_code in reversed(ko_stages):
                stage_matches = [m for m in ko_matches if m.get("stage") == stage_code]
                if stage_matches:
                    with st.expander(STAGE_MAP.get(stage_code, stage_code)):
                        for m in stage_matches:
                            display_match_item(m)

    # 【分頁2：分組賽 (動態刷新)】
    with tab2:
        st.subheader("48強分組賽動態賽程")
        group_matches = [m for m in all_matches if m.get("stage") == "GROUP_STAGE"]
        
        if not group_matches:
            st.info("⚽ 暫無分組賽程數據。")
        else:
            all_groups = sorted(list(set([m.get("group") for m in group_matches if m.get("group")])))
            for g_code in all_groups:
                g_matches = [m for m in group_matches if m.get("group") == g_code]
                with st.expander(f"📍 {GROUP_MAP.get(g_code, g_code)} 賽程進度與比分"):
                    for m in g_matches:
                        display_match_item(m)

    # 【分頁3：今日即時焦點】
    with tab3:
        st.subheader("開源伺服器當日同步")
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        if target_season == "2022":
            today_matches = [m for m in all_matches if m.get("stage") == "FINAL"]
        else:
            today_matches = [m for m in all_matches if m.get("utcDate", "").startswith(today_str)]
            
        if not today_matches:
            st.info(f"⚽ 今日 ({today_str}) 暫無進行中的世界盃賽事。\n(提示：2026世界盃首場分組賽將於台北時間 6/12 正式開踢！)")
        else:
            st.success(f"✅ 成功同步今日 {len(today_matches)} 場賽事！")
            for match in today_matches:
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
                status_text = STATUS_MAP.get(status_raw, status_raw)
                
                st.markdown("---")
                st.markdown(f"### 🏟️ {home} 🆚 {away}")
                col1, col2, col3 = st.columns(3)
                col1.metric(label=home, value=h_score)
                col2.metric(label="賽事狀態", value=status_text)
                col3.metric(label=away, value=a_score)
