import streamlit as st
import random
import pandas as pd
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Dice Master Pro - Trịnh Thị Như Quỳnh")

# --- HỆ THỐNG CSS CHỮ SIÊU TO ---
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 28px !important; }
    h1 { font-size: 80px !important; color: #1e3c72; text-align: center; }
    h2 { font-size: 50px !important; color: #2a5298; border-bottom: 4px solid #1e3c72; }
    .stButton>button {
        width: 100% !important; height: 120px !important;
        font-size: 45px !important; font-weight: bold !important;
        background: linear-gradient(135deg, #e52d27, #b31217) !important;
        color: white !important; border-radius: 20px !important;
    }
    .dice-container {
        display: flex; justify-content: center; align-items: center;
        height: 300px; background: white; border-radius: 30px;
        box-shadow: inset 0 0 30px rgba(0,0,0,0.1); margin: 20px 0;
    }
    .dice-img { width: 180px; height: 180px; margin: 0 20px; }
    .author-footer {
        position: fixed; left: 30px; bottom: 30px; background-color: rgba(255, 255, 255, 0.9);
        padding: 20px; border-radius: 12px; border-left: 10px solid #1e3c72;
        font-size: 30px; font-weight: bold; color: #1e3c72; z-index: 1000;
    }
    .conclusion-box {
        background-color: #fff9c4; padding: 30px; border-radius: 20px;
        border: 5px dashed #fbc02d; font-size: 36px; color: #000; margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM PHÁT ÂM THANH ---
def play_sound(sound_type):
    sound_urls = {
        "dice": "https://www.soundjay.com/misc/sounds/dice-roll-1.mp3",
        "click": "https://www.soundjay.com/buttons/sounds/button-16.mp3"
    }
    st.components.v1.html(f"""<script>var audio = new Audio("{sound_urls[sound_type]}"); audio.play();</script>""", height=0)

# --- HIỂN THỊ TÁC GIẢ ---
st.markdown(f"""<div class="author-footer">Giáo viên: Trịnh Thị Như Quỳnh<br>Trường THCS Trần Hưng Đạo</div>""", unsafe_allow_html=True)

st.write("# 🎲 MÔ PHỎNG XÁC SUẤT")
col_left, col_center, col_right = st.columns([1.2, 1.4, 1.4])

with col_left:
    st.write("## ⚙️ Thiết lập")
    num_dice = st.radio("1. Chọn số lượng xúc xắc:", [1, 2], horizontal=True)
    
    # DANH SÁCH BÀI TOÁN MỞ RỘNG
    if num_dice == 1:
        events = {
            "Mặt chấm là số chẵn (2, 4, 6)": lambda x: x[0] % 2 == 0,
            "Mặt chấm là số lẻ (1, 3, 5)": lambda x: x[0] % 2 != 0,
            "Mặt chấm là số nguyên tố (2, 3, 5)": lambda x: x[0] in [2, 3, 5],
            "Mặt chấm là số chính phương (1, 4)": lambda x: x[0] in [1, 4],
            "Mặt chấm lớn hơn 4 (5, 6)": lambda x: x[0] > 4,
            "Mặt chấm chia hết cho 3 (3, 6)": lambda x: x[0] % 3 == 0
        }
    else:
        events = {
            "Tổng số chấm là số chẵn": lambda x: sum(x) % 2 == 0,
            "Tổng số chấm là số lẻ": lambda x: sum(x) % 2 != 0,
            "Tổng số chấm bằng 7": lambda x: sum(x) == 7,
            "Tổng số chấm lớn hơn 9 (10, 11, 12)": lambda x: sum(x) > 9,
            "Hai mặt chấm giống nhau (Số kép)": lambda x: x[0] == x[1],
            "Tích số chấm là số chẵn": lambda x: (x[0] * x[1]) % 2 == 0,
            "Hiệu số chấm bằng 0": lambda x: abs(x[0] - x[1]) == 0,
            "Hiệu số chấm bằng 1": lambda x: abs(x[0] - x[1]) == 1
        }
        
    selected_event = st.selectbox("2. Chọn bài toán (Biến cố):", list(events.keys()))
    num_trials = st.select_slider("3. Số lần gieo:", options=[10, 100, 500, 1000, 5000], value=100)

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

    placeholder.markdown("<div class='dice-container'><p style='color:#ccc; font-size:40px;'>Sẵn sàng gieo...</p></div>", unsafe_allow_html=True)

    if st.button("🚀 GIEO XÚC XẮC"):
        play_sound("dice")
        placeholder.markdown(f"<div class='dice-container'><img src='{urls['rolling']}' class='dice-img'></div>", unsafe_allow_html=True)
        time.sleep(1.2)
        
        results = []
        for _ in range(num_trials):
            r1 = random.randint(1, 6)
            r2 = random.randint(1, 6) if num_dice == 2 else None
            results.append((r1, r2) if r2 else (r1,))
        st.session_state.all_data = results
        
        last = results[-1]
        html_res = f"<div class='dice-container'><img src='{urls[last[0]]}' class='dice-img'>"
        if num_dice == 2:
            html_res += f"<img src='{urls[last[1]]}' class='dice-img'>"
        html_res += "</div>"
        placeholder.markdown(html_res, unsafe_allow_html=True)

    if 'all_data' in st.session_state:
        st.write("### 📊 Thống kê tần suất")
        df = pd.DataFrame(st.session_state.all_data)
        val_sum = df[0] if num_dice == 1 else df[0] + df[1]
        counts = val_sum.value_counts().sort_index().reset_index()
        counts.columns = ['Giá trị mặt/Tổng', 'Số lần xuất hiện']
        st.table(counts)

with col_right:
    st.write("## 📈 Kết quả")
    if 'all_data' in st.session_state:
        check = events[selected_event]
        success_count = sum(1 for r in st.session_state.all_data if check(r))
        prob_exp = success_count / num_trials
        
        st.write(f"**Biến cố:** {selected_event}")
        st.metric("XÁC SUẤT THỰC NGHIỆM", f"{prob_exp:.2%}")
        st.progress(prob_exp)
        
        st.markdown(f"""
            <div class="conclusion-box">
                <b>📌 KẾT LUẬN:</b><br>
                Trong {num_trials} lần gieo, biến cố xảy ra {success_count} lần.<br>
                Khi số lần gieo càng lớn, xác suất thực nghiệm này sẽ càng ổn định và sát với xác suất lý thuyết.
            </div>
            """, unsafe_allow_html=True)
