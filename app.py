import streamlit as st
import random
import pandas as pd
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Xác suất - Trịnh Thị Như Quỳnh")

# --- HỆ THỐNG CSS CHỮ SIÊU TO CHO TIVI ---
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 26px !important; }
    h1 { font-size: 70px !important; color: #1e3c72; text-align: center; margin-bottom: 20px; }
    h2 { font-size: 45px !important; color: #2a5298; border-bottom: 3px solid #1e3c72; }
    
    /* Nút bấm khổng lồ */
    .stButton>button {
        width: 100% !important; height: 100px !important;
        font-size: 40px !important; font-weight: bold !important;
        background: linear-gradient(135deg, #e52d27, #b31217) !important;
        color: white !important; border-radius: 20px !important;
    }
    
    /* Khung chứa xúc xắc */
    .dice-container {
        display: flex; justify-content: center; align-items: center;
        height: 300px; background: white; border-radius: 30px;
        box-shadow: inset 0 0 30px rgba(0,0,0,0.1); margin: 20px 0; border: 1px solid #ddd;
    }
    .dice-img { width: 170px; height: 170px; margin: 0 20px; }
    
    /* Tác giả góc trái */
    .author-footer {
        position: fixed; left: 30px; bottom: 30px; background-color: rgba(255, 255, 255, 0.9);
        padding: 15px; border-radius: 12px; border-left: 10px solid #1e3c72;
        font-size: 26px; font-weight: bold; color: #1e3c72; z-index: 1000;
    }
    
    /* Đồng hồ đếm ngược */
    .timer-box {
        text-align: center; background: #000; color: #ff0000;
        font-family: 'Courier New', Courier, monospace;
        font-size: 75px; padding: 10px; border-radius: 15px; border: 4px solid #333;
    }
    
    /* Khung Lý thuyết & Kết luận */
    .theory-box {
        background-color: #f0f7ff; padding: 25px; border-radius: 15px;
        border: 2px solid #2196f3; font-size: 28px; margin-bottom: 25px;
    }
    .conclusion-box {
        background-color: #fff9c4; padding: 25px; border-radius: 15px;
        border: 4px dashed #fbc02d; font-size: 32px; color: #000; margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM PHÁT ÂM THANH ---
def play_sound(sound_type):
    sound_urls = {
        "dice": "https://www.soundjay.com/misc/sounds/dice-roll-1.mp3",
        "timer": "https://www.soundjay.com/buttons/sounds/beep-07.mp3"
    }
    st.components.v1.html(f"""<script>var audio = new Audio("{sound_urls[sound_type]}"); audio.play();</script>""", height=0)

# --- HIỂN THỊ TÁC GIẢ ---
st.markdown(f"""<div class="author-footer">Giáo viên: Trịnh Thị Như Quỳnh<br>Trường THCS Trần Hưng Đạo</div>""", unsafe_allow_html=True)

st.write("# 🎲 THỰC NGHIỆM XÁC SUẤT")

col_left, col_center, col_right = st.columns([1.1, 1.4, 1.5])

# --- CỘT 1: THIẾT LẬP ---
with col_left:
    st.write("## ⚙️ Thiết lập")
    num_dice = st.radio("1. Số xúc xắc:", [1, 2], horizontal=True)
    
    if num_dice == 1:
        events = {
            "Mặt chấm chẵn": {"fn": lambda x: x[0] % 2 == 0, "theory": "3/6 = 0.5", "t_val": 0.5, "sample": "{2; 4; 6}"},
            "Mặt chấm lẻ": {"fn": lambda x: x[0] % 2 != 0, "theory": "3/6 = 0.5", "t_val": 0.5, "sample": "{1; 3; 5}"},
            "Mặt nguyên tố (2,3,5)": {"fn": lambda x: x[0] in [2,3,5], "theory": "3/6 = 0.5", "t_val": 0.5, "sample": "{2; 3; 5}"},
            "Mặt chấm > 4": {"fn": lambda x: x[0] > 4, "theory": "2/6 ≈ 0.33", "t_val": 2/6, "sample": "{5; 6}"},
            "Mặt 6 chấm": {"fn": lambda x: x[0] == 6, "theory": "1/6 ≈ 0.17", "t_val": 1/6, "sample": "{6}"}
        }
    else:
        events = {
            "Tổng bằng 7": {"fn": lambda x: sum(x) == 7, "theory": "6/36 ≈ 0.17", "t_val": 6/36, "sample": "{(1,6); (2,5); (3,4); (4,3); (5,2); (6,1)}"},
            "Hai mặt giống nhau": {"fn": lambda x: x[0] == x[1], "theory": "6/36 ≈ 0.17", "t_val": 6/36, "sample": "{(1,1); (2,2); (3,3); (4,4); (5,5); (6,6)}"},
            "Tổng là số lẻ": {"fn": lambda x: sum(x) % 2 != 0, "theory": "18/36 = 0.5", "t_val": 0.5, "sample": "18 cặp số lẻ"},
            "Tổng lớn hơn 9": {"fn": lambda x: sum(x) > 9, "theory": "6/36 ≈ 0.17", "t_val": 6/36, "sample": "{(4,6); (5,5); (5,6); (6,4); (6,5); (6,6)}"}
        }
        
    selected_name = st.selectbox("2. Chọn biến cố:", list(events.keys()))
    num_trials = st.select_slider("3. Số lần gieo:", options=[10, 100, 500, 1000, 2000], value=100)

    st.write("---")
    st.write("## ⏱️ Thảo luận")
    timer_val = st.number_input("Số giây:", min_value=5, max_value=300, value=60)
    if st.button("🔔 BẮT ĐẦU ĐẾM"):
        t_place = st.empty()
        for i in range(timer_val, -1, -1):
            m, s = divmod(i, 60)
            t_place.markdown(f"<div class='timer-box'>{m:02d}:{s:02d}</div>", unsafe_allow_html=True)
            if i == 0: play_sound("timer")
            time.sleep(1)

# --- CỘT 2: HOẠT ĐỘNG ---
with col_center:
    st.write("## 🎰 Hoạt động")
    placeholder = st.empty()
    urls = {
        1: "https://upload.wikimedia.org/wikipedia/commons/1/1b/Dice-1-b.svg",
        2: "https://upload.wikimedia.org/wikipedia/commons/5/5f/Dice-2-b.svg",
        3: "https://upload.wikimedia.org/wikipedia/commons/b/b1/Dice-3-b.svg",
        4: "https://upload.wikimedia.org/wikipedia/commons/f/fd/Dice-4-b.svg",
        5: "https://upload.wikimedia.org/wikipedia/commons/0/08/Dice-5-b.svg",
        6: "https://upload.wikimedia.org/wikipedia/commons/2/26/Dice-6-b.svg",
        "rolling": "https://upload.wikimedia.org/wikipedia/commons/a/a5/Dice_rolling.gif"
    }

    placeholder.markdown("<div class='dice-container'><p style='color:#ccc;'>Nhấn nút để gieo...</p></div>", unsafe_allow_html=True)

    if st.button("🚀 GIEO XÚC XẮC"):
        play_sound("dice")
        placeholder.markdown(f"<div class='dice-container'><img src='{urls['rolling']}' class='dice-img'></div>", unsafe_allow_html=True)
        time.sleep(1.2)
        
        # Tạo kết quả ngẫu nhiên
        res = []
        for _ in range(num_trials):
            d1 = random.randint(1,6)
            d2 = random.randint(1,6) if num_dice == 2 else None
            res.append((d1, d2))
        st.session_state.
