import streamlit as st
import random
import pandas as pd

# Thiết lập trang chế độ rộng để phù hợp 16:9
st.set_page_config(layout="wide", page_title="Mô phỏng Xác suất Xúc xắc")

st.title("🎲 Công cụ Mô phỏng Xác suất Xúc xắc (Toán THCS)")

# --- KHỞI TẠO LAYOUT ---
# Chia tỉ lệ: 1/4 (Trái), 3/8 (Trung tâm), 3/8 (Phải) 
# (Tỉ lệ tương đối: 1 : 1.5 : 1.5)
col_left, col_center, col_right = st.columns([1, 1.5, 1.5])

# --- PHẦN GÓC BÊN TRÁI: ĐIỀU KHIỂN ---
with col_left:
    st.header("⚙️ Cấu hình")
    num_dice = st.radio("Chọn số lượng xúc xắc:", [1, 2], horizontal=True)
    
    # Danh sách biến cố tùy theo số xúc xắc
    if num_dice == 1:
        events = {
            "Mặt xuất hiện có số chấm là số chẵn": lambda x: x[0] % 2 == 0,
            "Mặt xuất hiện có số chấm lớn hơn 4": lambda x: x[0] > 4,
            "Mặt xuất hiện có số chấm là số nguyên tố": lambda x: x[0] in [2, 3, 5],
            "Mặt xuất hiện có số chấm nhỏ hơn 3": lambda x: x[0] < 3,
            "Mặt xuất hiện có số chấm chia hết cho 3": lambda x: x[0] % 3 == 0
        }
    else:
        events = {
            "Tổng số chấm bằng 7": lambda x: sum(x) == 7,
            "Tổng số chấm là một số chia hết cho 3": lambda x: sum(x) % 3 == 0,
            "Hai mặt xuất hiện giống nhau (số kép)": lambda x: x[0] == x[1],
            "Tổng số chấm lớn hơn 10": lambda x: sum(x) > 10,
            "Có ít nhất một mặt 6 chấm": lambda x: 6 in x,
            "Tích số chấm là một số lẻ": lambda x: (x[0] * x[1]) % 2 != 0
        }
    
    selected_event_name = st.selectbox("Chọn biến cố cần theo dõi:", list(events.keys()))
    num_trials = st.number_input("Số lần thực nghiệm (tối đa 10.000):", 
                                 min_value=1, max_value=10000, value=100)
    
    run_sim = st.button("🚀 Bắt đầu gieo", use_container_width=True)

# --- LOGIC MÔ PHỎNG ---
results = []
if 'sim_data' not in st.session_state:
    st.session_state.sim_data = None

if run_sim:
    # Mô phỏng gieo xúc xắc
    sim_results = []
    for _ in range(num_trials):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6) if num_dice == 2 else None
        res = (die1,) if die2 is None else (die1, die2)
        sim_results.append(res)
    st.session_state.sim_data = sim_results

# --- MÀN HÌNH TRUNG TÂM: HOẠT ĐỘNG & BẢNG SỐ LIỆU ---
with col_center:
    st.header("🎰 Hoạt động")
    if st.session_state.sim_data:
        # Hiển thị kết quả lần cuối cùng (mô phỏng hoạt động dừng lại)
        last_roll = st.session_state.sim_data[-1]
        st.subheader("Kết quả lần gieo cuối:")
        c1, c2 = st.columns(2)
        with c1: st.metric("Xúc xắc 1", last_roll[0])
        if num_dice == 2:
            with c2: st.metric("Xúc xắc 2", last_roll[1])
        
        # Thống kê số lần xuất hiện
        st.subheader("📊 Bảng thống kê số lần xuất hiện")
        df = pd.DataFrame(st.session_state.sim_data, columns=["Xúc xắc 1", "Xúc xắc 2"] if num_dice == 2 else ["Mặt"])
        
        if num_dice == 1:
            counts = df["Mặt"].value_counts().sort_index()
            st.table(counts)
        else:
            df['Tổng'] = df["Xúc xắc 1"] + df["Xúc xắc 2"]
            sum_counts = df['Tổng'].value_counts().sort_index()
            st.table(sum_counts)

# --- MÀN HÌNH BÊN PHẢI: LÝ THUYẾT & XÁC SUẤT ---
with col_right:
    st.header("🧠 Phân tích")
    
    show_sample_space = st.toggle("Hiện Không gian mẫu (Ω)")
    if show_sample_space:
        if num_dice == 1:
            st.write("$\Omega = \{1; 2; 3; 4; 5; 6\}$")
            st.write("$n(\Omega) = 6$")
        else:
            st.write("$\Omega = \{(1,1), (1,2), ..., (6,6)\}$")
            st.write("$n(\Omega) = 36$")
            
    show_prob = st.toggle("Hiện Xác suất của biến cố")
    if show_prob and st.session_state.sim_data:
        # Tính toán xác suất thực nghiệm
        check_func = events[selected_event_name]
        favorable_outcomes = sum(1 for res in st.session_state.sim_data if check_func(res))
        exp_prob = favorable_outcomes / num_trials
        
        st.info(f"**Biến cố A:** '{selected_event_name}'")
        st.write(f"- Số lần thuận lợi: $n(A) = {favorable_outcomes}$")
        st.write(f"- Xác suất thực nghiệm: $P(A) \approx {exp_prob:.4f}$")
        
        # Thanh tiến trình minh họa xác suất
        st.progress(exp_prob)import streamlit as st
import random
import pandas as pd
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Dice Master Pro - Trịnh Thị Như Quỳnh")

# --- HỆ THỐNG CSS ĐẶC BIỆT (CHỮ SIÊU TO - GIAO DIỆN CHUYÊN NGHIỆP) ---
st.markdown("""
    <style>
    /* 1. Phóng to chữ toàn bộ trang để học sinh ngồi xa quan sát rõ */
    html, body, [class*="st-"] {
        font-size: 28px !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* 2. Tiêu đề chính siêu lớn */
    h1 { font-size: 85px !important; color: #1e3c72; text-align: center; margin-bottom: 30px !important; }
    h2 { font-size: 55px !important; color: #2a5298; border-bottom: 4px solid #1e3c72; padding-bottom: 10px; }
    
    /* 3. Tăng kích thước các lựa chọn (Selectbox, Radio) */
    .stSelectbox label, .stRadio label { font-size: 35px !important; font-weight: bold !important; color: #333; }
    
    /* 4. Nút bấm GIEO XÚC XẮC khổng lồ và hiệu ứng */
    .stButton>button {
        width: 100% !important;
        height: 140px !important;
        font-size: 50px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #e52d27, #b31217) !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        box-shadow: 0 12px 24px rgba(0,0,0,0.4) !important;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 15px 30px rgba(0,0,0,0.5) !important; }

    /* 5. Khung xúc xắc tập trung */
    .dice-container {
        display: flex; justify-content: center; align-items: center;
        height: 320px; background: #ffffff; border-radius: 40px;
        box-shadow: inset 0 0 40px rgba(0,0,0,0.1); margin: 25px 0;
        border: 2px solid #ddd;
    }
    .dice-img { width: 200px; height: 200px; margin: 0 30px; }

    /* 6. Thông tin tác giả cố định ở góc dưới */
    .author-footer {
        position: fixed;
        left: 30px;
        bottom: 30px;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #1e3c72;
        font-size: 32px;
        font-weight: bold;
        color: #1e3c72;
        z-index: 1000;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    /* 7. Kết luận sư phạm nổi bật */
    .conclusion-box {
        background-color: #fff9c4;
        padding: 30px;
        border-radius: 20px;
        border: 5px dashed #fbc02d;
        font-size: 38px;
        color: #000;
        margin-top: 40px;
        line-height: 1.5;
    }

    /* 8. Bảng số liệu rõ nét */
    .stTable { font-size: 38px !important; width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM PHÁT ÂM THANH (Dice & Click) ---
def play_sound(sound_type):
    sound_urls = {
        "dice": "https://www.soundjay.com/misc/sounds/dice-roll-1.mp3",
        "click": "https://www.soundjay.com/buttons/sounds/button-16.mp3"
    }
    st.components.v1.html(f"""
        <script>
            var audio = new Audio("{sound_urls[sound_type]}");
            audio.play();
        </script>
    """, height=0)

# --- HIỂN THỊ TÁC GIẢ ---
st.markdown(f"""
    <div class="author-footer">
        Giáo viên: Nguyễn Thị Như Quỳnh<br>
        Trường THCS Trần Hưng Đạo
    </div>
    """, unsafe_allow_html=True)

# --- GIAO DIỆN CHÍNH ---
st.write("# 🎲 MÔ PHỎNG XÁC SUẤT")

col_left, col_center, col_right = st.columns([1, 1.5, 1.5])

# --- CỘT 1: CÀI ĐẶT (1/4 màn hình) ---
with col_left:
    st.write("## ⚙️ Thiết lập")
    num_dice = st.radio("1. Số lượng xúc xắc:", [1, 2], horizontal=True)
    
    if num_dice == 1:
        events = {
            "Mặt chấm là số chẵn": lambda x: x[0] % 2 == 0,
            "Mặt chấm lẻ": lambda x: x[0] % 2 != 0,
            "Mặt chấm ≥ 4": lambda x: x[0] >= 4,
            "Mặt 6 chấm": lambda x: x[0] == 6
        }
    else:
        events = {
            "Tổng số chấm là số chẵn": lambda x: sum(x) % 2 == 0,
            "Tổng số chấm bằng 7": lambda x: sum(x) == 7,
            "Tổng số chấm chia hết cho 3": lambda x: sum(x) % 3 == 0,
            "Ít nhất một mặt 6": lambda x: 6 in x
        }
        
    selected_event = st.selectbox("2. Chọn biến cố:", list(events.keys()))
    num_trials = st.select_slider("3. Số lần gieo thực nghiệm:", 
                                   options=[10, 100, 500, 1000, 5000, 10000], value=100)

# --- CỘT 2: HOẠT ĐỘNG (Trung tâm) ---
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

    # Ban đầu hiển thị hộp xúc xắc trống
    placeholder.markdown("<div class='dice-container'><p style='color:#ccc; font-size:40px;'>Sẵn sàng gieo...</p></div>", unsafe_allow_html=True)

    if st.button("🚀 BẮT ĐẦU GIEO"):
        play_sound("dice")
        # Hiệu ứng chuyển động (GIF)
        placeholder.markdown(f"<div class='dice-container'><img src='{urls['rolling']}' class='dice-img'></div>", unsafe_allow_html=True)
        time.sleep(1.5)
        
        # Mô phỏng toán học
        all_results = []
        for _ in range(num_trials):
            r1 = random.randint(1, 6)
            r2 = random.randint(1, 6) if num_dice == 2 else None
            all_results.append((r1, r2) if r2 else (r1,))
        st.session_state.all_data = all_results
        
        # Kết quả lần gieo cuối
        last = all_results[-1]
        html_res = f"<div class='dice-container'><img src='{urls[last[0]]}' class='dice-img'>"
        if num_dice == 2:
            html_res += f"<img src='{urls[last[1]]}' class='dice-img'>"
        html_res += "</div>"
        placeholder.markdown(html_res, unsafe_allow_html=True)

    # Hiển thị bảng số liệu thống kê
    if 'all_data' in st.session_state:
        st.write("### 📊 Thống kê số lần xuất hiện")
        df = pd.DataFrame(st.session_state.all_data)
        val_sum = df[0] if num_dice == 1 else df[0] + df[1]
        counts = val_sum.value_counts().sort_index().reset_index()
        counts.columns = ['Giá trị mặt', 'Số lần xuất hiện']
        st.table(counts)

# --- CỘT 3: KẾT QUẢ & PHÂN TÍCH (Bên phải) ---
with col_right:
    st.write("## 📈 Kết quả")
    
    show_sample = st.toggle("Hiện/Ẩn Không gian mẫu (Ω)")
    if show_sample:
        if num_dice == 1: st.code("Ω = {1, 2, 3, 4, 5, 6}", language="text")
        else: st.code("Ω = {(1,1), (1,2), ..., (6,6)} -> 36 kết quả", language="text")

    if 'all_data' in st.session_state:
        check = events[selected_event]
        success_count = sum(1 for r in st.session_state.all_data if check(r))
        prob_exp = success_count / num_trials
        
        st.write(f"**Biến cố đang xét:** {selected_event}")
        st.metric("XÁC SUẤT THỰC NGHIỆM", f"{prob_exp:.2%}")
        st.progress(prob_exp)
        st.write(f"👉 Xuất hiện {success_count} lần trong tổng số {num_trials} lần thực nghiệm.")
        
        # KẾT LUẬN SƯ PHẠM ĐỂ CHỐT KIẾN THỨC
        st.markdown(f"""
            <div class="conclusion-box">
                <b>📌 MỐI LIÊN HỆ QUAN TRỌNG:</b><br>
                Khi số lần thực nghiệm <b>n</b> ({num_trials} lần) càng <b>lớn</b>, 
                xác suất thực nghiệm sẽ càng tiến dần đến (xấp xỉ bằng) xác suất lý thuyết của biến cố đó.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Mời cô Như Quỳnh và các em nhấn nút để xem kết quả phân tích!")

