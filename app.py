import streamlit as st
import random
import pandas as pd
import time

# 1. Cấu hình màn hình tràn tỉ lệ 16:9
st.set_page_config(layout="wide", page_title="Mô phỏng Xúc xắc 3D")

# 2. CSS để tạo giao diện và hiệu ứng xúc xắc
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .dice-box {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
        background: white;
        border-radius: 20px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .dice-img {
        width: 120px;
        height: 120px;
        filter: drop-shadow(5px 5px 10px rgba(0,0,0,0.3));
    }
    .stButton>button {
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Hàm phát âm thanh bằng JavaScript (Vượt rào cản trình duyệt)
def play_sound():
    sound_url = "https://www.soundjay.com/misc/sounds/dice-roll-1.mp3"
    st.components.v1.html(f"""
        <script>
            var audio = new Audio("{sound_url}");
            audio.play().catch(e => console.log("Âm thanh bị chặn, cần tương tác trước"));
        </script>
    """, height=0)

# --- CHIA LAYOUT THEO TỈ LỆ 1/4 : 3/8 : 3/8 ---
col_left, col_center, col_right = st.columns([1, 1.5, 1.5])

# --- CỘT TRÁI (1/4): ĐIỀU KHIỂN ---
with col_left:
    st.subheader("⚙️ Cài đặt")
    num_dice = st.selectbox("Chọn số lượng xúc xắc", [1, 2])
    
    if num_dice == 1:
        events = {
            "Mặt chấm > 4": lambda x: x[0] > 4,
            "Mặt chấm lẻ": lambda x: x[0] % 2 != 0,
            "Mặt chấm chia hết cho 3": lambda x: x[0] % 3 == 0
        }
    else:
        events = {
            "Tổng số chấm chia hết cho 3": lambda x: sum(x) % 3 == 0,
            "Tổng số chấm là số nguyên tố": lambda x: sum(x) in [2,3,5,7,11],
            "Xuất hiện ít nhất một mặt 6": lambda x: 6 in x
        }
        
    selected_event = st.selectbox("Chọn biến cố", list(events.keys()))
    num_trials = st.select_slider("Số lần thực nghiệm", options=[10, 50, 100, 500, 1000, 5000], value=100)
    
    btn_run = st.button("🎲 BẮT ĐẦU GIEO")

# --- CỘT GIỮA (3/8): HOẠT ĐỘNG VÀ BẢNG THỐNG KÊ ---
with col_center:
    st.subheader("🎰 Mô phỏng hoạt động")
    placeholder_dice = st.empty()
    
    # URL ảnh xúc xắc (Sử dụng ảnh tĩnh chất lượng cao từ Wikimedia)
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
        play_sound() # Phát âm thanh
        # Hiệu ứng đang gieo (Hiện GIF)
        with placeholder_dice.container():
            st.markdown(f"""<div class='dice-box'><img src='{dice_urls["rolling"]}' class='dice-img'></div>""", unsafe_allow_html=True)
        
        time.sleep(1.5) # Chờ 1.5 giây để học sinh hồi hộp
        
        # Tính toán kết quả thực tế
        all_results = []
        for _ in range(num_trials):
            r1 = random.randint(1, 6)
            r2 = random.randint(1, 6) if num_dice == 2 else None
            all_results.append((r1, r2) if r2 else (r1,))
        
        st.session_state.data = all_results
        
        # Hiện kết quả cuối cùng (Ảnh tĩnh)
        last = all_results[-1]
        with placeholder_dice.container():
            html = "<div class='dice-box'>"
            html += f"<img src='{dice_urls[last[0]]}' class='dice-img'>"
            if num_dice == 2:
                html += f"<img src='{dice_urls[last[1]]}' class='dice-img' style='margin-left:20px'>"
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

    # Bảng thống kê số lần xuất hiện
    if 'data' in st.session_state:
        df = pd.DataFrame(st.session_state.data)
        if num_dice == 1:
            stats = df[0].value_counts().sort_index().reset_index()
            stats.columns = ['Mặt chấm', 'Số lần xuất hiện']
        else:
            df['Tổng'] = df[0] + df[1]
            stats = df['Tổng'].value_counts().sort_index().reset_index()
            stats.columns = ['Tổng số chấm', 'Số lần xuất hiện']
        
        st.write("**Bảng kết quả thực nghiệm:**")
        st.dataframe(stats, use_container_width=True)

# --- CỘT PHẢI (3/8): PHÂN TÍCH ---
with col_right:
    st.subheader("📊 Phân tích kết quả")
    
    show_sample = st.toggle("Hiện Không gian mẫu (Ω)")
    if show_sample:
        if num_dice == 1: st.code("Ω = {1, 2, 3, 4, 5, 6}")
        else: st.code("Ω = {(1,1), (1,2), ..., (6,6)} -> 36 kết quả")

    show_prob = st.toggle("Hiện Xác suất biến cố")
    if show_prob and 'data' in st.session_state:
        check_fn = events[selected_event]
        success_count = sum(1 for r in st.session_state.data if check_fn(r))
        prob_exp = success_count / num_trials
        
        st.success(f"Biến cố: {selected_event}")
        st.metric("Xác suất thực nghiệm P(A)", f"{prob_exp:.2%}")
        st.info(f"Giải thích: Xuất hiện {success_count} lần trong tổng số {num_trials} lần gieo.")
        st.progress(prob_exp)
