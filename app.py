import streamlit as st
import requests
from datetime import datetime

# ==========================================
# 1. API 參數設定區 (原廠金鑰)
# ==========================================
API_KEY = "92d87d7767e403abc4ca3d8adbcca6fc"

# ==========================================
# 2. 自動連網抓取函式 (破解免費版限制邏輯)
# ==========================================
@st.cache_data(ttl=60)
def fetch_scores(is_test_mode=False):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_KEY}
    
    if is_test_mode:
        # 【破解限制 1】測試模式：不給日期，直接要 2022 全年資料
        querystring = {"league": "1", "season": "2022"}
    else:
        # 【破解限制 2】正式模式：不要整個 2026 賽季，改要「當天」的即時資料
        today_str = datetime.now().strftime("%Y-%m-%d")
        querystring = {"league": "1", "date": today_str}
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            
            # 攔截並顯示原廠的字典格式錯誤
            if res_json.get("errors"):
                err_msg = res_json['errors']
                # 如果錯誤是字典格式，轉成文字顯示
                if isinstance(err_msg, dict):
                    err_msg = " | ".join([f"{k}: {v}" for k, v in err_msg.items()])
                return {"error": f"原廠限制：{err_msg}"}
            
            data = res_json.get("response", [])
            
            # 如果是測試模式，拿到 64 場比賽後，只截取最後一場 (阿根廷 vs 法國決賽)
            if is_test_mode and len(data) > 0:
                data = [data[-1]]
                
            return {"data": data}
            
        elif response.status_code == 429:
            return {"error": "API 每日免費額度已用盡，請明天再試！"}
        else:
            return {"error": f"伺服器錯誤代碼：{response.status_code}"}
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
st.set_page_config(page_title="世足賽程與比分", page_icon="🏆", layout="centered")

st.title("🏆 2026 世足賽程與即時比分")
st.markdown("美加墨聯合主辦｜賽程表與自動同步比分系統")

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
    st.subheader("國際伺服器自動同步")
    
    mode = st.radio("賽季選擇：", ["測試模式 (2022決賽)", "正式模式 (今日賽況)"], horizontal=True)
    
    if st.button("🔄 立即同步最新比分", use_container_width=True):
        st.cache_data.clear()
        
    if mode == "測試模式 (2022決賽)":
        result = fetch_scores(is_test_mode=True)
    else:
        result = fetch_scores(is_test_mode=False)

    # 顯示結果與排版
    if "error" in result:
        st.error(f"❌ {result['error']}")
    elif not result.get("data"):
        st.info("⚽ 該日或賽季目前無比賽資料。 (提示：2026正式賽事尚未開打)")
    else:
        matches = result["data"]
        st.success(f"✅ 成功同步 {len(matches)} 場賽事！")
        
        for match in matches:
            home = match.get("teams", {}).get("home", {}).get("name", "未知名稱")
            away = match.get("teams", {}).get("away", {}).get("name", "未知名稱")
            h_score = match.get("goals", {}).get("home", 0)
            a_score = match.get("goals", {}).get("away", 0)
            status = match.get("fixture", {}).get("status", {}).get("short", "未知狀態")
            
            st.markdown("---")
            st.markdown(f"### 🏟️ {home} 🆚 {away}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric(label=home, value=h_score)
            col2.metric(label="賽事狀態", value=status)
            col3.metric(label=away, value=a_score)
