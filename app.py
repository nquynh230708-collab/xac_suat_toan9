import streamlit as st
import random
import pandas as pd
import time

# 1. Cấu hình màn hình tỉ lệ 16:9
st.set_page_config(layout="wide", page_title="Mô phỏng Xúc xắc 3D Pro")

# 2. CSS để tạo giao diện
st.markdown("""
    <style>
    .dice-box {
        display: flex; justify-content: center; align-items: center;
        height: 200px; background: white; border-radius: 20px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .dice-img { width: 120px; height: 120px; }
    .stButton>button {
        background: linear-gradient(135deg, #FF4B2B, #FF416C);
        color: white; font-weight: bold; border-radius: 15px; border: none; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HÀM PHÁT ÂM THANH MẠNH MẼ (Dùng JavaScript nhúng)
def play_sound_js():
    # Sử dụng link âm thanh ổn định
    sound_url = "https://www.soundjay.com/misc/sounds/dice-roll-1.mp3"
    st.components.v1.html(f"""
        <script>
            var audio = new Audio("{sound_url}");
            audio.play();
        </script>
    """, height=0)

# --- CHIA LAYOUT 1/4 : 3/8 : 3/8 ---
col_left, col_center, col_right = st.columns([1, 1.5, 1.5])

# CỘT TRÁI
with col_left:
    st.header("⚙️ Cài đặt")
    num_dice = st.selectbox("Số lượng xúc xắc", [1, 2])
    num_trials = st.select_slider("Số lần thực nghiệm", options=[10, 100, 500, 1000], value=100)
    
    events = {
        "Mặt chấm lẻ": lambda x: x[0] % 2 != 0,
        "Tổng chia hết cho 3": lambda x: sum(x) % 3 == 0 if len(x)>1 else x[0] % 3 == 0,
        "Tổng bằng 7": lambda x: sum(x) == 7 if len(x)>1 else False
    }
    selected_event = st.selectbox("Chọn biến cố", list(events.keys()))
    
    # NÚT BẤM KÍCH HOẠT
    btn_run = st.button("🎲 GIEO NGAY")

# CỘT GIỮA
with col_center:
    st.header("🎰 Hoạt động")
    placeholder = st.empty()
    
    dice_urls = {
        1: "https://upload.wikimedia.org/wikipedia/commons/1/1b/Dice-1-b.svg",
        2: "https://upload.wikimedia.org/wikipedia/commons/5/5f/Dice-2-b.svg",
        3: "https://upload.wikimedia.org/wikipedia/commons/b/b1/Dice-3-b.svg",
        4: "https://upload.wikimedia.org/wikipedia/commons/f/fd/Dice-4-b.svg",
        5: "https://upload.wikimedia.org/wikipedia/commons/0/08/Dice-5-b.svg",
        6: "https://upload.wikimedia.org/wikipedia/commons/2/26/Dice-6-b.svg",
        "rolling": "https://upload.wikimedia.org/wikipedia/commons/a/a5/Dice_rolling.gif"
    }

    if btn_run:
        # PHÁT ÂM THANH NGAY KHI BẤM NÚT
        play_sound_js()
        
        # Hiệu ứng gieo
        placeholder.markdown(f"<div class='dice-box'><img src='{dice_urls['rolling']}' class='dice-img'></div>", unsafe_allow_html=True)
        time.sleep(1.2)
        
        # Tính kết quả
        results = []
        for _ in range(num_trials):
            r1 = random.randint(1, 6)
            r2 = random.randint(1, 6) if num_dice == 2 else None
            results.append((r1, r2) if r2 else (r1,))
        st.session_state.data = results
        
        # Hiện kết quả cuối
        last = results[-1]
        html = f"<div class='dice-box'><img src='{dice_urls[last[0]]}' class='dice-img'>"
        if num_dice == 2:
            html += f"<img src='{dice_urls[last[1]]}' class='dice-img' style='margin-left:20px'>"
        html += "</div>"
        placeholder.markdown(html, unsafe_allow_html=True)

    if 'data' in st.session_state:
        df = pd.DataFrame(st.session_state.data)
        st.write("**Bảng tần suất:**")
        st.dataframe(df[0].value_counts().sort_index() if num_dice==1 else (df[0]+df[1]).value_counts().sort_index())

# CỘT PHẢI
with col_right:
    st.header("📊 Phân tích")
    if 'data' in st.session_state:
        check = events[selected_event]
        success = sum(1 for r in st.session_state.data if check(r))
        prob = success / num_trials
        st.metric("Xác suất thực nghiệm", f"{prob:.2%}")
        st.progress(prob)
        st.info(f"Biến cố xảy ra {success} lần trên {num_trials} lần thử.")
