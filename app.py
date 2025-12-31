import streamlit as st
import random
import pandas as pd
import plotly.express as px
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Mô phỏng Xúc xắc 3D")

# --- CSS VÀ JAVASCRIPT ĐỂ TẠO HÌNH ẢNH & ÂM THANH ---
st.markdown("""
    <style>
    /* 1. Tạo hình ảnh mặt xúc xắc bằng CSS */
    .dice-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 20px 0;
    }
    .die {
        width: 100px;
        height: 100px;
        background-color: white;
        border: 4px solid #333;
        border-radius: 15px;
        position: relative;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
    }
    /* Các chấm tròn trên mặt xúc xắc */
    .dot {
        width: 18px;
        height: 18px;
        background-color: #e74c3c;
        border-radius: 50%;
        position: absolute;
    }
    /* Vị trí các chấm (tối đa 6 chấm) */
    .dot-center { top: 50%; left: 50%; transform: translate(-50%, -50%); }
    .dot-top-left { top: 15%; left: 15%; }
    .dot-top-right { top: 15%; right: 15%; }
    .dot-mid-left { top: 50%; left: 15%; transform: translateY(-50%); }
    .dot-mid-right { top: 50%; right: 15%; transform: translateY(-50%); }
    .dot-bot-left { bottom: 15%; left: 15%; }
    .dot-bot-right { bottom: 15%; right: 15%; }

    /* 2. Hiệu ứng rung lắc mạnh */
    @keyframes shake {
        0% { transform: rotate(0deg) scale(1); }
        25% { transform: rotate(10deg) scale(1.1); }
        50% { transform: rotate(-10deg) scale(0.9); }
        75% { transform: rotate(5deg) scale(1.1); }
        100% { transform: rotate(0deg) scale(1); }
    }
    .rolling { animation: shake 0.2s infinite; }
    </style>
    """, unsafe_allow_html=True)

# Hàm vẽ mặt xúc xắc bằng HTML (Dùng cho cả lúc đang quay và kết quả)
def get_dice_html(value, is_rolling=False):
    dots = ""
    if value == 1: dots = '<div class="dot dot-center"></div>'
    elif value == 2: dots = '<div class="dot dot-top-left"></div><div class="dot dot-bot-right"></div>'
    elif value == 3: dots = '<div class="dot dot-top-left"></div><div class="dot dot-center"></div><div class="dot dot-bot-right"></div>'
    elif value == 4: dots = '<div class="dot dot-top-left"></div><div class="dot dot-top-right"></div><div class="dot dot-bot-left"></div><div class="dot dot-bot-right"></div>'
    elif value == 5: dots = '<div class="dot dot-top-left"></div><div class="dot dot-top-right"></div><div class="dot dot-center"></div><div class="dot dot-bot-left"></div><div class="dot dot-bot-right"></div>'
    elif value == 6: dots = '<div class="dot dot-top-left"></div><div class="dot dot-top-right"></div><div class="dot dot-mid-left"></div><div class="dot dot-mid-right"></div><div class="dot dot-bot-left"></div><div class="dot dot-bot-right"></div>'
    
    roll_class = "rolling" if is_rolling else ""
    return f'<div class="die {roll_class}">{dots}</div>'

# Hàm kích hoạt âm thanh bằng JavaScript
def play_dice_sound():
    sound_url = "https://www.soundjay.com/misc/sounds/dice-roll-1.mp3"
    st.components.v1.html(f"""
        <script>
            var audio = new Audio("{sound_url}");
            audio.play();
        </script>
    """, height=0)

# --- GIAO DIỆN CHÍNH ---
st.title("🎲 Trình mô phỏng Xác suất Học đường")

col_left, col_center, col_right = st.columns([1, 1.5, 1.5])

# --- CỘT TRÁI: ĐIỀU KHIỂN ---
with col_left:
    st.header("⚙️ Cài đặt")
    num_dice = st.radio("Số lượng xúc xắc:", [1, 2], horizontal=True)
    num_trials = st.number_input("Số lần thực nghiệm:", 1, 10000, 100)
    
    if num_dice == 1:
        events = {"Mặt > 4": lambda x: x[0] > 4, "Mặt chẵn": lambda x: x[0] % 2 == 0}
    else:
        events = {"Tổng chia hết cho 3": lambda x: sum(x) % 3 == 0, "Tổng bằng 7": lambda x: sum(x) == 7}
    
    selected_event = st.selectbox("Biến cố quan sát:", list(events.keys()))
    btn_roll = st.button("🚀 BẮT ĐẦU GIEO", use_container_width=True)

# --- CỘT GIỮA: HIỆN THỊ HÌNH ẢNH & BIỂU ĐỒ ---
with col_center:
    st.header("🎰 Hoạt động")
    dice_placeholder = st.empty()
    
    if btn_roll:
        play_dice_sound() # Kích hoạt âm thanh
        
        # Chạy hiệu ứng quay xúc xắc trong 1 giây
        for _ in range(10):
            d1_temp, d2_temp = random.randint(1, 6), random.randint(1, 6)
            html = f'<div class="dice-container">{get_dice_html(d1_temp, True)}'
            if num_dice == 2: html += get_dice_html(d2_temp, True)
            html += '</div>'
            dice_placeholder.markdown(html, unsafe_allow_html=True)
            time.sleep(0.1)
        
        # Tính kết quả thực tế
        all_results = []
        for _ in range(num_trials):
            r = (random.randint(1,6), random.randint(1,6) if num_dice==2 else None)
            all_results.append(r)
        
        st.session_state.all_results = all_results
        
        # Hiện kết quả cuối cùng (không rung nữa)
        last = all_results[-1]
        html_final = f'<div class="dice-container">{get_dice_html(last[0], False)}'
        if num_dice == 2: html_final += get_dice_html(last[1], False)
        html_final += '</div>'
        dice_placeholder.markdown(html_final, unsafe_allow_html=True)

    # Vẽ biểu đồ bảng thống kê bên dưới
    if 'all_results' in st.session_state:
        df = pd.DataFrame(st.session_state.all_results)
        val_col = df[0] if num_dice == 1 else df[0] + df[1].fillna(0)
        counts = val_col.value_counts().sort_index().reset_index()
        counts.columns = ['Giá trị', 'Số lần']
        st.table(counts)

# --- CỘT PHẢI: KHÔNG GIAN MẪU & XÁC SUẤT ---
with col_right:
    st.header("📊 Phân tích")
    show_sample = st.checkbox("Hiện Không gian mẫu (Ω)")
    if show_sample:
        if num_dice == 1: st.write("$\Omega = \{1, 2, 3, 4, 5, 6\}$")
        else: st.write("$n(\Omega) = 36$ kết quả có thể xảy ra.")
        
    if 'all_results' in st.session_state:
        check_fn = events[selected_event]
        success = sum(1 for r in st.session_state.all_results if check_fn(r))
        prob = success / num_trials
        
        st.info(f"**Biến cố:** {selected_event}")
        st.metric("Xác suất thực nghiệm", f"{prob:.2%}")
        st.progress(prob)
