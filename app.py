import streamlit as st
import pandas as pd

# 設定網頁標題與手機版面適應
st.set_page_config(page_title="2026世足賽程表", page_icon="⚽", layout="centered")

st.title("⚽ 2026 世足 48 強完整賽程")
st.markdown("**首度由美、加、墨 3 國聯合主辦，賽期長達 39 天！**")

# 決賽資訊卡片
st.info("🏆 **季軍戰**: 7月19日 05:00\n\n🏆 **決賽**: 7月20日 03:00 (紐約賽區大都會人壽體育場)")

st.subheader("小組賽名單與賽程 (台灣時間)")

# 賽程資料字典
world_cup_data = {
    "A組": {"teams": "墨西哥、南非、韓國、捷克", "dates": "6/12、6/19、6/25"},
    "B組": {"teams": "加拿大、波赫、卡達、瑞士", "dates": "6/13、6/14、6/19、6/25"},
    "C組": {"teams": "巴西、摩洛哥、海地、蘇格蘭", "dates": "6/14、6/20、6/25"},
    "D組": {"teams": "美國、巴拉圭、澳大利亞、土耳其", "dates": "6/13、6/14、6/20、6/26"},
    "E組": {"teams": "德國、古拉索、象牙海岸、厄瓜多", "dates": "6/15、6/21、6/26"},
    "F組": {"teams": "荷蘭、日本、瑞典、突尼西亞", "dates": "6/15、6/21、6/26"},
    "G組": {"teams": "比利時、埃及、伊朗、紐西蘭", "dates": "6/16、6/22、6/27"},
    "H組": {"teams": "西班牙、維德角、沙烏地阿拉伯、烏拉圭", "dates": "6/16、6/22、6/27"},
    "I組": {"teams": "法國、塞內加爾、伊拉克、挪威", "dates": "6/17、6/23、6/27"},
    "J組": {"teams": "阿根廷、阿爾及利亞、奧地利、約旦", "dates": "6/17、6/23、6/28"},
    "K組": {"teams": "葡萄牙、剛果、烏茲別克、哥倫比亞", "dates": "6/18、6/24、6/28"},
    "L組": {"teams": "英格蘭、克羅埃西亞、迦納、巴拿馬", "dates": "6/18、6/24、6/28"},
}

# 使用 Expander 讓手機閱讀更友善
for group, info in world_cup_data.items():
    with st.expander(f"📍 {group}"):
        st.write(f"**參賽隊伍**：{info['teams']}")
        st.write(f"**比賽日期**：{info['dates']}")