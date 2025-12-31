import streamlit as st
import random
import pandas as pd
import time

# 1. CẤU HÌNH TRANG RỘNG
st.set_page_config(layout="wide", page_title="Dice Master Pro - Trịnh Thị Như Quỳnh")

# 2. HỆ THỐNG CSS ĐẶC BIỆT CHO TRÌNH CHIẾU TIVI (CHỮ SIÊU TO)
st.markdown("""
    <style>
    /* Phóng to chữ toàn bộ trang */
    html, body, [class*="st-"] {
        font-size: 30px !important; /* Cỡ chữ cực đại cho học sinh ngồi xa */
        font-family: 'Arial', sans-serif;
    }
    
    /* Chỉnh cỡ chữ cho các tiêu đề */
    h1 { font-size: 80px !important; color: #1e3c72; text-align: center; }
    h2 { font-size: 55px !important; color: #2a5298; border-bottom: 3px solid #ccc; }
    h3 { font-size: 45px !important; }

    /* Phóng to nút bấm gieo */
    .stButton>button {
        width: 100% !important;
        height: 120px !important;
        font-size: 45px !important;
        font-weight: bold !important;
        background: linear-gradient(135deg, #FF4B2B, #FF416C) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3) !important;
    }

    /* Khung hiển thị xúc xắc */
    .dice-container {
        display: flex; justify-content: center; align-items: center;
        height: 300px; background: white; border-radius: 30px;
        box-shadow: inset 0 0 30px rgba(0,0,0,0.1); margin: 20px 0;
    }
    .dice-img { width: 180px; height: 180px; margin: 0 20px; }

    /* Thông tin tác giả góc trái dưới */
    .author-footer {
        position: fixed;
        left: 30px;
        bottom: 30px;
        background-color: rgba(255, 255, 255, 0.8);
        padding: 15px;
        border-radius: 10px;
        border-left: 8px solid #1e3c72;
        font-size: 28px;
        color: #333;
        z-index: 1000;
        line-height: 1.4;
    }

    /* Bảng số liệu to */
    .stTable { font-size: 35px !important; }
    
    /* Kết luận sư phạm */
    .conclusion-box {
        background-color: #fff9c4;
        padding: 25px;
        border-radius: 15px;
        border: 4px dashed #fbc02d;
        font-size: 32px;
        color: #000;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HÀM PHÁT ÂM THANH
def trigger_sound(sound_type):
    urls = {
        "dice": "https://www.soundjay.com/misc/sounds/dice-roll-1.mp3",
        "click": "https://www.soundjay.com/buttons/sounds/button-16.mp3"
    }
    st.components.v1.html(f"""
        <script>
            var audio = new Audio("{urls[sound_type]}");
            audio.play();
        </script>
    """, height=0)

# 4. HIỂN THỊ THÔNG TIN TÁC GIẢ
st.markdown(f"""
    <div class="author-footer">
        <b>Giáo viên:</b> Nguyễn Thị Như Quỳnh<br>
        <b>Trường:</b> THCS Trần Hưng Đạo
    </div>
    """, unsafe_allow_html=True)

# 5. GIAO DIỆN CHÍNH
st.write("# 🎲 MÔ PHỎNG XÚC XẮC")

col_left, col_center, col_right = st.columns([1, 1.5, 1.5])

# --- CỘT 1: CÀI ĐẶT ---
with col_left:
    st.write("## ⚙️ Cài đặt")
    num_dice = st.radio("Chọn số xúc xắc:", [1, 2], horizontal=True)
    
    if num_dice == 1:
        events = {
            "Mặt chấm lẻ": lambda x: x[0] % 2 != 0,
            "Mặt chấm >= 4": lambda x: x[0] >= 4,
            "Mặt 6 chấm": lambda x: x[0] == 6
        }
    else:
        events = {
            "Tổng là số chẵn": lambda x: sum(x) % 2 == 0,
            "Tổng bằng 7": lambda x: sum(x) == 7,
            "Ít nhất một mặt 6": lambda x: 6 in x
        }
        
    selected_event = st.selectbox("Biến cố quan sát:", list(events.keys()))
    num_trials = st.select_slider("Số lần gieo:", options=[10, 100, 500, 1000, 5000], value=100)

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

    if st.button("🚀 GIEO XÚC XẮC"):
        trigger_sound("dice")
        # Hiệu ứng gieo
        placeholder.markdown(f"<div class='dice-container'><img src='{urls['rolling']}' class='dice-img'></div>", unsafe_allow_html=True)
        time.sleep(1.5)
        
        # Tính kết quả
        results = []
        for _ in range(num_trials):
            r1 = random.randint(1, 6)
            r2 = random.randint(1, 6) if num_dice == 2 else None
            results.append((r1, r2) if r2 else (r1,))
        st.session_state.results = results
        
        # Hiện kết quả cuối
        last = results[-1]
        html = f"<div class='dice-container'><img src='{urls[last[0]]}' class='dice-img'>"
        if num_dice == 2:
            html += f"<img src='{urls[last[1]]}' class='dice-img'>"
        html += "</div>"
        placeholder.markdown(html, unsafe_allow_html=True)

    if 'results' in st.session_state:
        st.write("### 📝 Thống kê tần suất")
        df = pd.DataFrame(st.session_state.results)
        val_col = df[0] if num_dice == 1 else df[0] + df[1]
        counts = val_col.value_counts().sort_index().reset_index()
        counts.columns = ['Giá trị', 'Số lần']
        st.table(counts)

# --- CỘT 3: KẾT LUẬN ---
with col_right:
    st.write("## 📊 Phân tích")
    if 'results' in st.session_state:
        check_fn = events[selected_event]
        success_count = sum(1 for r in st.session_state.results if check_fn(r))
        prob = success_count / num_trials
        
        st.write(f"**Biến cố:** {selected_event}")
        st.metric("Xác suất thực nghiệm", f"{prob:.2%}")
        st.progress(prob)
        
        # CÂU KẾT LUẬN CỦA GIÁO VIÊN
        st.markdown(f"""
            <div class="conclusion-box">
                <b>💡 Ghi nhớ:</b><br>
                Khi số lần gieo <b>n</b> ngày càng lớn (thực nghiệm nhiều lần), 
                xác suất thực nghiệm sẽ càng gần với xác suất lý thuyết. 
                Đây chính là mối liên hệ mật thiết giữa thực hành và lý thuyết trong toán học!
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Mời cô nhấn nút 'GIEO XÚC XẮC' để bắt đầu phân tích kết quả.")

