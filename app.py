import streamlit as st
import random
import pandas as pd
import time

# 1. Cấu hình màn hình tỉ lệ 16:9
st.set_page_config(layout="wide", page_title="Dice Master Pro - Nguyễn Thị Như Quỳnh")

# 2. CSS NÂNG CẤP: Tăng kích thước chữ và tùy chỉnh giao diện
st.markdown("""
    <style>
    /* Tăng cỡ chữ toàn bộ ứng dụng */
    html, body, [class*="st-"] {
        font-size: 24px !important; /* Gấp đôi cỡ chữ bình thường */
    }
    h1 { font-size: 4rem !important; }
    h2 { font-size: 3rem !important; }
    h3 { font-size: 2.5rem !important; }
    
    /* Tăng kích thước nút bấm */
    .stButton>button {
        height: 80px !important;
        font-size: 30px !important;
        border-radius: 15px !important;
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
    }
    
    /* Thông tin tác giả */
    .author-info {
        position: fixed;
        left: 20px;
        bottom: 20px;
        font-size: 22px;
        color: #555;
        border-left: 5px solid #1e3c72;
        padding-left: 10px;
        z-index: 100;
    }
    
    /* Hiệu ứng xúc xắc */
    .dice-box {
        display: flex; justify-content: center; align-items: center;
        height: 250px; background: #fff; border-radius: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .dice-img { width: 150px; height: 150px; }
    
    /* Phóng to bảng số liệu */
    .stDataFrame td, .stDataFrame th { font-size: 22px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Hàm phát âm thanh (Xúc xắc & Click)
def play_sound(sound_type="dice"):
    sounds = {
        "dice": "https://www.soundjay.com/misc/sounds/dice-roll-1.mp3",
        "click": "https://www.soundjay.com/buttons/sounds/button-16.mp3"
    }
    st.components.v1.html(f"""
        <script>
            var audio = new Audio("{sounds[sound_type]}");
            audio.play();
        </script>
    """, height=0)

# --- THÔNG TIN TÁC GIẢ GÓC TRÁI DƯỚI ---
st.markdown("""
    <div class="author-info">
        <b>Giáo viên:</b> Nguyễn Thị Như Quỳnh<br>
        <b>Trường:</b> THCS Trần Hưng Đạo
    </div>
    """, unsafe_allow_html=True)

st.title("🎲 Mô phỏng Xác suất Xúc xắc")

# --- CHIA LAYOUT 1/4 : 3/8 : 3/8 ---
col_left, col_center, col_right = st.columns([1, 1.5, 1.5])

with col_left:
    st.header("⚙️ Cài đặt")
    num_dice = st.selectbox("Số lượng xúc xắc", [1, 2], on_change=lambda: play_sound("click"))
    
    if num_dice == 1:
        events = {
            "Mặt chấm lẻ": lambda x: x[0] % 2 != 0,
            "Mặt chấm > 3": lambda x: x[0] > 3,
            "Mặt chấm là số nguyên tố": lambda x: x[0] in [2, 3, 5]
        }
    else:
        events = {
            "Tổng số chấm là số chẵn": lambda x: sum(x) % 2 == 0,
            "Tổng số chấm chia hết cho 3": lambda x: sum(x) % 3 == 0,
            "Tổng số chấm bằng 7": lambda x: sum(x) == 7
        }
    
    selected_event = st.selectbox("Chọn biến cố", list(events.keys()), on_change=lambda: play_sound("click"))
    num_trials = st.select_slider("Số lần thực nghiệm", options=[10, 100, 500, 1000, 5000], value=100)
    
    # Nút bấm chính
    btn_run = st.button("🚀 BẮT ĐẦU GIEO")

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
        play_sound("dice") # Âm thanh gieo xúc xắc
        placeholder.markdown(f"<div class='dice-box'><img src='{dice_urls['rolling']}' class='dice-img'></div>", unsafe_allow_html=True)
        time.sleep(1.2)
        
        results = []
        for _ in range(num_trials):
            r1 = random.randint(1, 6)
            r2 = random.randint(1, 6) if num_dice == 2 else None
            results.append((r1, r2) if r2 else (r1,))
        st.session_state.data = results
        
        last = results[-1]
        html = f"<div class='dice-box'><img src='{dice_urls[last[0]]}' class='dice-img'>"
        if num_dice == 2:
            html += f"<img src='{dice_urls[last[1]]}' class='dice-img' style='margin-left:30px'>"
        html += "</div>"
        placeholder.markdown(html, unsafe_allow_html=True)

    if 'data' in st.session_state:
        df = pd.DataFrame(st.session_state.data)
        st.write("### 📊 Bảng tần suất:")
        if num_dice == 1:
            stats = df[0].value_counts().sort_index()
        else:
            stats = (df[0]+df[1]).value_counts().sort_index()
        st.table(stats)

with col_right:
    st.header("🔍 Kết quả")
    if 'data' in st.session_state:
        check = events[selected_event]
        success = sum(1 for r in st.session_state.data if check(r))
        prob = success / num_trials
        
        st.metric("Xác suất thực nghiệm", f"{prob:.2%}")
        st.progress(prob)
        
        st.markdown(f"""
        <div style="background-color: #e1f5fe; padding: 20px; border-radius: 10px; border-left: 10px solid #01579b;">
            <p><b>📝 Kết luận:</b> Khi số lần thực nghiệm (n = {num_trials}) càng <b>lớn</b>, 
            xác suất thực nghiệm sẽ càng tiến gần đến xác suất lý thuyết của biến cố.</p>
        </div>
        """, unsafe_allow_html=True)
