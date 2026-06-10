import streamlit as st
import requests
from datetime import datetime

# ==========================================
# 1. API 設定區 (已綁定您超穩定的 Football-Data.org 金鑰)
# ==========================================
API_TOKEN = "d5921a999fd5418aa3c5026db3889cf2"

# ==========================================
# 2. 自動連網抓取函式 (Football-Data.org 專用)
# ==========================================
@st.cache_data(ttl=60)
def fetch_scores(season="2026"):
    url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": API_TOKEN}
    params = {"season": season}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return {"data": response.json().get("matches", [])}
        elif response.status_code == 429:
            return {"error": "已達到每分鐘請求次數限制，請等候一分鐘後再刷新。"}
        elif response.status_code == 403:
            msg = response.json().get("message", "權限不足，可能無法存取歷史或特定賽季資料。")
            return {"error": f"原廠權限限制 (403)：{msg}"}
        else:
            return {"error": f"國際伺服器回應錯誤 (代碼 {response.status_code})"}
    except Exception as e:
        return {"error": f"系統連線異常：{e}"}

# ==========================================
# 3. 2026 賽程靜態資料庫 (台北時間)
# ==========================================
group_matches = {
    "A組": ["6/12 03:00 墨西哥 VS 南非", "6/12 10:00 韓國 VS 捷克", "6/19 00:00 捷克 VS 南非", "6/19 09:00 墨西哥 VS 韓國", "6/25 09:00 南非 VS 韓國", "6/25 09:00 捷克 VS 墨西哥"],
    "B組": ["6/13 03:00 加拿大 VS 波赫", "6/14 03:00 卡達 VS 瑞士", "6/19 03:00 波赫 VS 瑞士", "6/19 06:00 加拿大 VS 卡達", "6/25 03:00 瑞士 VS 加拿大", "6/25 03:00 波赫 VS 卡達"],
    "C組": ["6/14 06:00 巴西 VS 摩洛哥", "6/14 09:00 海地 VS 蘇格蘭", "6/20 06:00 蘇格蘭 VS 摩洛哥", "6/20 08:30 巴西 VS 海地", "6/25 06:00 摩洛哥 VS 海地", "6/25 06:00 蘇格蘭 VS 巴西"],
    "D組": ["6/13 09:00 美國 VS 巴拉圭", "6/14 12:00 澳大利亞 VS 土耳其", "6/20 03:00 美國 VS 澳大利亞", "6/20 11:00 土耳其 VS 巴拉圭", "6/26 10:00 土耳其 VS 美國", "6/26 10:00 巴拉圭 VS 澳大利亞"],
    "E組": ["6/15 01:00 德國 VS 古拉索", "6/15 07:00 象牙海岸 VS 厄瓜多", "6/21 04:00 德國 VS 象牙海岸", "6/21 08:00 厄瓜多 VS 古拉索", "6/26 04:00 古拉索 VS 象牙海岸", "6/26 04:00 厄瓜多 VS 德國"],
    "F組": ["6/15 04:00 荷蘭 VS 日本", "6/15 10:00 瑞典 VS 突尼西亞", "6/21 01:00 荷蘭 VS 瑞典", "6/21 12:00 突尼西亞 VS 日本", "6/26 07:00 突尼西亞 VS 荷蘭", "6/26 07:00 日本 VS 瑞典"],
    "G組": ["6/16 03:00 比利時 VS 埃及", "6/16 09:00 伊朗 VS 紐西蘭", "6/22 03:00 比利時 VS 伊朗", "6/22 09:00 紐西蘭 VS 埃及", "6/27 11:00 紐西蘭 VS 比利時", "6/27 11:00 埃及 VS 伊朗"],
    "H組": ["6/16 00:00 西班牙 VS 維德角", "6/16 06:00 沙烏地 VS 烏拉圭", "6/22 00:00 西班牙 VS 沙烏地", "6/22 06:00 烏拉圭 VS 維德角", "6/27 08:00 維德角 VS 沙烏地", "6/27 08:00 烏拉圭 VS 西班牙"],
    "I組": ["6/17 03:00 法國 VS 塞內加爾", "6/17 06:00 伊拉克 VS 挪威", "6/23 05:00 法國 VS 伊拉克", "6/23 08:00 挪威 VS 塞內加爾", "6/27 03:00 挪威 VS 法國", "6/27 03:00 塞內加爾 VS 伊拉克"],
    "J組": ["6/17 09:00 阿根廷 VS 阿爾及利亞", "6/17 12:00 奧地利 VS 約旦", "6/23 01:00 阿根廷 VS 奧地利", "6/23 11:00 約旦 VS 阿爾及利亞", "6/28 10:00 阿爾及利亞 VS 奧地利", "6/28 10:00 約旦 VS 阿根廷"],
    "K組": ["6/18 01:00 葡萄牙 VS 剛果", "6/18 10:00 烏茲別克 VS 哥倫比亞", "6/24 01:00 葡萄牙 VS 烏茲別克", "6/24 10:00 哥倫比亞 VS 剛果", "6/28 07:30 哥倫比亞 VS 葡萄牙", "6/28 07:30 剛果 VS 烏茲別克"],
    "L組": ["6/18 04:00 英格蘭 VS 克羅埃西亞", "6/18 07:00 迦納 VS 巴拿馬", "6/24 04:00 英格蘭 VS 迦納", "6/24 07:00 巴拿馬 VS 克羅埃西亞", "6/28 05:00 巴拿馬 VS 英格蘭", "6/28 05:00 克羅埃西亞 VS 迦納"]
}

knockout_matches = {
    "🏆 冠軍戰 & 季軍戰": ["7/20 03:00 [決賽] 4強勝方1 VS 4強勝方2", "7/19 05:00 [季軍戰] 4強敗方1 VS 4強敗方2"],
    "⭐ 4強賽 (共2場)": ["7/15 06:00 [4強賽1] 8強勝方1 VS 8強勝方2", "7/16 06:00 [4強賽2] 8強勝方3 VS 8強勝方4"],
    "⚔️ 8強賽 (共4場)": ["7/10 06:00 [8強賽1] 16強勝方1 VS 16強勝方2", "7/11 01:00 [8強賽2] 16強勝方3 VS 16強勝方4", "7/11 06:00 [8強賽3] 16強勝方5 VS 16強勝方6", "7/12 06:00 [8強賽4] 16強勝方7 VS 16強勝方8"],
    "🎯 16強賽 (共8場)": ["7/05 01:00 [16強賽1] 32強勝方1 VS 32強勝方2", "7/05 06:00 [16強賽2] 32強勝方3 VS 32強勝方4", "7/06 01:00 [16強賽3] 32強勝方5 VS 32強勝方6", "7/06 06:00 [16強賽4] 32強勝方7 VS 32強勝方8", "7/07 01:00 [16強賽5] 32強勝方9 VS 32強勝方10", "7/07 06:00 [16強賽6] 32強勝方11 VS 32強勝方12", "7/08 01:00 [16強賽7] 32強勝方13 VS 32強勝方14", "7/08 06:00 [16強賽8] 32強勝方15 VS 32強勝方16"],
    "🚀 32強賽 (共16場)": ["6/29 01:00 [32強賽1] A組第1 VS 最佳第3名(1)", "6/29 06:00 [32強賽2] B組第2 VS C組第2", "6/30 01:00 [32強賽3] D組第1 VS 最佳第3名(2)", "6/30 06:00 [32強賽4] E組第1 VS 最佳第3名(3)", "6/30 10:00 [32強賽5] F組第1 VS 最佳第3名(4)", "7/01 01:00 [32強賽6] G組第2 VS H組第2", "7/01 06:00 [32強賽7] I組第1 VS 最佳第3名(5)", "7/01 10:00 [32強賽8] J組第1 VS 最佳第3名(6)", "7/02 01:00 [32強賽9] K組第1 VS 最佳第3名(7)", "7/02 06:00 [32強賽10] L組第1 VS 最佳第3名(8)", "7/02 10:00 [32強賽11] A組第2 VS B組第1", "7/03 01:00 [32強賽12] C組第1 VS D組第2", "7/03 06:00 [32強賽13] E組第2 VS F組第2", "7/03 10:00 [32強賽14] G組第1 VS H組第1", "7/04 01:00 [32強賽15] I組第2 VS J組第2", "7/04 06:00 [32強賽16] K組第2 VS L組第2"]
}

# ==========================================
# 4. 主程式介面與排版
# ==========================================
st.set_page_config(page_title="2026世足賽程與比分", page_icon="🏆", layout="centered")

st.title("🏆 2026 世足賽程與即時比分")
st.markdown("美加墨聯合主辦｜賽程表與開源自動同步比分系統")

tab1, tab2, tab3 = st.tabs(["🏆 淘汰賽", "⚽ 分組賽", "📡 即時戰況(自動)"])

with tab1:
    st.subheader("世界盃淘汰賽段")
    for stage, matches in knockout_matches.items():
        with st.expander(stage):
            for match in matches:
                st.markdown(f"🕒 **{match}**")

with tab2:
    st.subheader("48強分組賽段")
    for group, matches in group_matches.items():
        with st.expander(f"📍 {group}"):
            for match in matches:
                st.markdown(f"🕒 **{match}**")

with tab3:
    st.subheader("開源伺服器自動同步")
    
    mode = st.radio("賽季選擇：", ["測試模式 (2022決賽)", "正式模式 (今日即時)"], horizontal=True)
    
    if st.button("🔄 立即同步最新比分", use_container_width=True):
        st.cache_data.clear()
        
    display_matches = []
    is_error = False

    # 邏輯區分：測試模式完全離線不連網
    if mode == "測試模式 (2022決賽)":
        st.success("✅ 成功載入歷史測試資料！ (內建離線模式，不消耗 API 額度)")
        # 直接寫入 2022 決賽數據
        display_matches = [{
            "homeTeam": {"name": "Argentina"},
            "awayTeam": {"name": "France"},
            "score": {"fullTime": {"home": 3, "away": 3}},
            "status": "FINISHED"
        }]
    else:
        # 正式模式：連網抓取 2026
        result = fetch_scores(season="2026")
        if "error" in result:
            st.error(f"❌ {result['error']}")
            is_error = True
        else:
            all_matches = result.get("data", [])
            # 過濾出今天日期的賽事
            today_str = datetime.now().strftime("%Y-%m-%d")
            display_matches = [m for m in all_matches if m.get("utcDate", "").startswith(today_str)]
            
            if not display_matches:
                st.info(f"⚽ 今日 ({datetime.now().strftime('%Y-%m-%d')}) 暫無進行中的世界盃賽事。\n(提示：2026世界盃首場分組賽將於台北時間 6/12 03:00 正式開踢！)")
                is_error = True # 阻止下方渲染空白框
            else:
                st.success(f"✅ 成功獲取 {len(display_matches)} 場賽事資訊！")

    # 渲染比分畫面
    if not is_error and display_matches:
        status_map = {
            "FINISHED": "比賽結束", "IN_PLAY": "進行中", "PAUSED": "中場休息",
            "TIMED": "未開始", "SCHEDULED": "已排程", "POSTPONED": "延期"
        }
        
        for match in display_matches:
            home = match.get("homeTeam", {}).get("name", "未知名稱")
            away = match.get("awayTeam", {}).get("name", "未知名稱")
            
            score_data = match.get("score", {}).get("fullTime", {})
            h_score = score_data.get("home")
            a_score = score_data.get("away")
            h_score = 0 if h_score is None else h_score
            a_score = 0 if a_score is None else a_score
            
            status_raw = match.get("status", "UNKNOWN")
            status_text = status_map.get(status_raw, status_raw)
            
            st.markdown("---")
            st.markdown(f"### 🏟️ {home} 🆚 {away}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric(label=home, value=h_score)
            col2.metric(label="賽事狀態", value=status_text)
            col3.metric(label=away, value=a_score)
