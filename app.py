import streamlit as st
import random
import pandas as pd
import plotly.express as px
import time
import base64

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Dice Master 3D Pro")

# --- DỮ LIỆU ÂM THANH (Base64 encode để không cần file mp3 riêng lẻ) ---
# Đây là tiếng xúc xắc ngắn gọn được mã hóa sẵn để nhúng trực tiếp vào code
dice_sound_b64 = """
T2dnUwACAAAAAAAAAABQZnxAAAAAAABH81cBe0JvorU/N2F1ZGkueGlwaC5vcmcvZmxhYy8w
LjEuMy02NmVmNTFjOWEyZGMxYWM5YmI1NGIyZDk1ODFkZWE5OC9lbi53aWtpcGVkaWEub3Jn
L3dpa2kvQXVkaW9fc2lnbmFsX3Byb2Nlc3NpbmcgKEZMQUMpAAEEZW5jb2Rlci1pZCAgPT0g
djEuMS4wIChsaWJmbGFjIDEuMy4yKSAgLyAgc2VyaWFsLTIgPT0gMTEwNjE0ODg1NzAgIC8g
IHByZWRpY3Rvci1vcmRlciAgPT0gOCAgLyAgbWluLXBhcnRpdGlvbi1vcmRlciAgPT0gMCAg
LyAgbWF4LXBhcnRpdGlvbi1vcmRlciAgPT0gOCAgLyAgc2FtcGxlLXJhdGUgID09IDQ0MTAw
ICAvICBjaGFubmVscyAgPT0gMSAgLyAgYml0cy1wZXItc2FtcGxlICA9PSAxNgAgZGF0YQAA
ABcAAABXAAAAZwAAAFwAAABwAAAAWAAAAHIAAABNAAAAcgAAAEkAAAB8AAAAZAAAAJQAAAB/
AAAAoAAAAIcAAACyAAAAmAAAAMQAAACuAAAA4AAAAMIAAADuAAAA3gAAAPUAAAD1AAAA/wAA Let's pretend this is a full dice sound string for brevity. 
Ghi chú: Đoạn mã này là giả lập cho ngắn gọn. Trong thực tế bạn cần một chuỗi base64 mp3/ogg thực sự.
Để code chạy được ngay, tôi sẽ dùng một thủ thuật khác bên dưới.
"""
# HACK: Để đơn giản hóa việc copy-paste và đảm bảo chạy được ngay mà không cần chuỗi base64 dài dòng, 
# chúng ta sẽ dùng một link âm thanh ngắn có sẵn trên mạng.
sound_url = "https://www.soundjay.com/misc/sounds/dice-roll-1.mp3"

def play_sound():
    """Hàm chèn HTML ẩn để phát âm thanh"""
    sound_html = f"""
        <audio autoplay>
        <source src="{sound_url}" type="audio/mpeg">
        Your browser does not support the audio element.
        </audio>
    """
    # Nhúng vào một container rỗng để không hiện trình phát nhạc
    st.empty().markdown(sound_html, unsafe_allow_html=True)

# --- CSS TÙY CHỈNH (Tạo hiệu ứng 3D và Rung lắc) ---
st.markdown("""
    <style>
    /* Định nghĩa hiệu ứng rung lắc khi gieo */
    @keyframes shake {
      0% { transform: translate(1px, 1px) rotate(0deg); }
      10% { transform: translate(-1px, -2px) rotate(-1deg); }
      20% { transform: translate(-3px, 0px) rotate(1deg); }
      30% { transform: translate(3px, 2px) rotate(0deg); }
      40% { transform: translate(1px, -1px) rotate(1deg); }
      50% { transform: translate(-1px, 2px) rotate(-1deg); }
      60% { transform: translate(-3px, 1px) rotate(0deg); }
      70% { transform: translate(3px, 1px) rotate(-1deg); }
      80% { transform: translate(-1px, -1px) rotate(1deg); }
      90% { transform: translate(1px, 2px) rotate(0deg); }
      100% { transform: translate(1px, -2px) rotate(-1deg); }
    }

    /* Class áp dụng hiệu ứng rung */
    .rolling {
        animation: shake 0.5s;
        animation-iteration-count: infinite;
        opacity: 0.7;
    }

    /* Style cho xúc xắc 3D giả lập */
    .dice-3d {
        font-size: 100px;
        color: #d9534f; /* Màu đỏ của xúc xắc */
        text-shadow: 2px 2px 4px #000000, 4px 4px 0px #8c2b29; /* Tạo bóng đổ nổi khối */
        display: inline-block;
        margin: 10px;
        transition: all 0.3s ease;
    }
    
    .final-result {
        transform: scale(1.1); /* Phóng to nhẹ khi ra kết quả cuối */
    }

    .stButton>button { width: 100%; border-radius: 20px; height: 3em; font-weight: bold; background: linear-gradient(to right, #4e54c8, #8f94fb); color: white; border: none;}
    </style>
    """, unsafe_allow_html=True)

# Dictionary ánh xạ số sang icon Unicode
dice_icons = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}

st.title("🎲 Dice Master 3D Pro: Thử tài Xác suất")
st.divider()

# --- LAYOUT CHÍNH ---
col_left, col_center, col_right = st.columns([1, 1.5, 1.5])

# --- CỘT TRÁI: THIẾT LẬP & DỰ ĐOÁN ---
with col_left:
    st.subheader("🛠 Thiết lập & Dự đoán")
    num_dice = st.radio("Số lượng xúc xắc:", [1, 2], horizontal=True, key="num_dice_select")
    
    if num_dice == 1:
        events = {
            "Mặt chẵn": lambda x: x[0] % 2 == 0,
            "Số chấm > 4": lambda x: x[0] > 4,
            "Số nguyên tố (2,3,5)": lambda x: x[0] in [2, 3, 5],
        }
    else:
        events = {
            "Tổng bằng 7": lambda x: sum(x) == 7,
            "Tổng chẵn": lambda x: sum(x) % 2 == 0,
            "Số kép (Hai mặt giống nhau)": lambda x: x[0] == x[1],
        }
    
    selected_event = st.selectbox("Chọn biến cố:", list(events.keys()))
    num_trials = st.select_slider("Số lần gieo (N):", options=[10, 50, 100, 500, 1000], value=50)

    st.write("---")
    st.write("**🎯 Dự đoán của bạn:**")
    user_guess = st.slider("Bạn nghĩ xác suất là bao nhiêu %?", 0, 100, 50, key="guess_slider")
    
    btn_run = st.button("🎲 GIEO NGAY! (Có âm thanh)")

# --- XỬ LÝ LOGIC GIEO VÀ HIỆU ỨNG ---
if btn_run:
    # 1. Tạo placeholder để chứa hình ảnh xúc xắc
    dice_placeholder = col_center.empty()
    
    # 2. Phát âm thanh
    play_sound()
    
    # 3. Hiệu ứng hình ảnh: Vòng lặp thay đổi mặt liên tục (Giả lập đang gieo)
    for _ in range(12): # Chạy 12 khung hình trong khoảng 1.2 giây
        temp_d1 = random.randint(1, 6)
        if num_dice == 2:
            temp_d2 = random.randint(1, 6)
            # Hiển thị icon với class 'rolling' và 'dice-3d'
            dice_placeholder.markdown(f"""
                <div style='text-align: center;' class='rolling'>
                    <span class='dice-3d'>{dice_icons[temp_d1]}</span>
                    <span class='dice-3d'>{dice_icons[temp_d2]}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            dice_placeholder.markdown(f"""
                <div style='text-align: center;' class='rolling'>
                    <span class='dice-3d'>{dice_icons[temp_d1]}</span>
                </div>
            """, unsafe_allow_html=True)
        time.sleep(0.1) # Dừng 0.1s mỗi khung hình

    # 4. Tính toán kết quả thực tế sau khi hiệu ứng kết thúc
    final_results = []
    for _ in range(num_trials):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6) if num_dice == 2 else None
        final_results.append((d1, d2) if d2 else (d1,))
    
    st.session_state.final_results = final_results
    st.session_state.last_roll = final_results[-1]

# --- CỘT GIỮA: KẾT QUẢ CUỐI CÙNG & ĐỒ THỊ ---
with col_center:
    # Nếu không phải đang chạy nút bấm mà đã có kết quả trong session
    if not btn_run and 'last_roll' in st.session_state:
         dice_placeholder = st.empty() # Tạo lại placeholder nếu cần

    if 'last_roll' in st.session_state:
        # Hiển thị kết quả mặt cuối cùng (Dừng lại, không rung nữa, thêm class final-result)
        last = st.session_state.last_roll
        if num_dice == 2:
             dice_placeholder.markdown(f"""
                <div style='text-align: center;'>
                    <span class='dice-3d final-result'>{dice_icons[last[0]]}</span>
                    <span class='dice-3d final-result'>{dice_icons[last[1]]}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
             dice_placeholder.markdown(f"""
                <div style='text-align: center;'>
                    <span class='dice-3d final-result'>{dice_icons[last[0]]}</span>
                </div>
            """, unsafe_allow_html=True)

    st.write("---")
    # Biểu đồ tần suất (như cũ)
    if 'final_results' in st.session_state:
        df = pd.DataFrame(st.session_state.final_results)
        if num_dice == 1:
            data_counts = df[0].value_counts().sort_index().reset_index()
            data_counts.columns = ['Mặt', 'Số lần']
            fig = px.bar(data_counts, x='Mặt', y='Số lần', color='Số lần', title=f"Tần suất trong {num_trials} lần gieo")
        else:
            df['Tổng'] = df[0] + df[1]
            data_counts = df['Tổng'].value_counts().sort_index().reset_index()
            fig = px.bar(data_counts, x='index', y='Tổng', color='Tổng', title=f"Tần suất Tổng trong {num_trials} lần gieo")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

# --- CỘT PHẢI: TÍNH ĐIỂM & SO SÁNH ---
with col_right:
    st.subheader("🏆 Kết quả & Điểm số")
    if 'final_results' in st.session_state:
        check_fn = events[selected_event]
        success_count = sum(1 for r in st.session_state.final_results if check_fn(r))
        actual_prob = (success_count / num_trials) * 100
        
        # Tính điểm
        error = abs(user_guess - actual_prob)
        score = max(0, 100 - int(error * 1.5)) # Phạt nặng hơn nếu sai số lớn

        st.metric("Xác suất Thực nghiệm (P')", f"{actual_prob:.1f}%", delta=f"{actual_prob - user_guess:.1f}% so với dự đoán")
        
        st.write("---")
        st.write(f"**Độ chính xác dự đoán:** {score}/100 điểm")
        progress_bar = st.progress(score)

        if score >= 90:
            st.balloons()
            st.success("Wow! Trực giác xác suất tuyệt vời! 🎉")
        elif score >= 70:
            st.info("Rất tốt! Bạn dự đoán khá sát. 👍")
        elif score >= 50:
            st.warning("Tạm ổn. Hãy thử tăng số lần gieo xem sao. 🤔")
        else:
            st.error("Chưa chính xác lắm. Xác suất thực tế khác xa dự đoán! 😅")

    else:
        st.info("👈 Đặt dự đoán ở cột bên trái rồi nhấn nút GIEO NGAY!")import streamlit as st
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

        st.progress(exp_prob)
