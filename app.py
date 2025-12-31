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
        st.progress(exp_prob)