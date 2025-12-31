import streamlit as st
import random
import pandas as pd
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Dice Master Pro - Trịnh Thị Như Quỳnh")

# --- HỆ THỐNG CSS CHỮ SIÊU TO & GIAO DIỆN ---
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 26px !important; }
    h1 { font-size: 70px !important; color: #1e3c72; text-align: center; margin-bottom: 20px; }
    h2 { font-size: 45px !important; color: #2a5298; border-bottom: 3px solid #1e3c72; }
    
    .stButton>button {
        width: 100% !important; height: 100px !important;
        font-size: 40px !important; font-weight: bold !important;
        background: linear-gradient(135deg, #e52d27, #b31217) !important;
        color: white !important; border-radius: 20px !important;
    }
    
    .dice-container {
        display: flex; justify-content: center; align-items: center;
        height: 280px; background: white; border-radius: 30px;
        box-shadow: inset 0 0 30px rgba(0,0,0,0.1); margin: 20px 0;
    }
    .dice-img { width: 160px; height: 160px; margin: 0 20px; }
    
    .author-footer {
        position: fixed; left: 30px; bottom: 30px; background-color: rgba(255, 255, 255, 0.9);
        padding: 15px; border-radius: 12px; border-left: 10px solid #1e3c72;
        font-size: 26px; font-weight: bold; color: #1e3c72; z-index: 1000;
    }
    
    .timer-box {
        text-align: center; background: #000; color: #ff0000;
        font-family: 'Courier New', Courier, monospace;
        font-size: 60px; padding: 10px; border-radius: 15px; border: 4px solid #333;
    }
    
    .theory-box {
        background-color: #e3f2fd; padding: 20px; border-radius: 15px;
        border-left: 10px solid #2196f3; font-size: 28px; margin-bottom: 20px;
    }
    
    .conclusion-box {
        background-color: #fff9c4; padding: 25px; border-radius: 15px;
        border: 4px dashed #fbc02d; font-size: 32px; color: #000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HÀM PHÁT ÂM THANH ---
def play_sound(sound_type):
    sound_urls = {
        "dice": "https://www.soundjay.com/misc/sounds/dice-roll-1.mp3",
        "timer": "https://www.soundjay.com/buttons/sounds/beep-07.mp3",
        "click": "https://www.soundjay.com/buttons/sounds/button-16.mp3"
    }
    st.components.v1.html(f"""<script>var audio = new Audio("{sound_urls[sound_type]}"); audio.play();</script>""", height=0)

# --- HIỂN THỊ TÁC GIẢ ---
st.markdown(f"""<div class="author-footer">Giáo viên: Trịnh Thị Như Quỳnh<br>Trường THCS Trần Hưng Đạo</div>""", unsafe_allow_html=True)

st.write("# 🎲 THỰC NGHIỆM XÁC SUẤT")
col_left, col_center, col_right = st.columns([1.1, 1.4, 1.5])

# --- CỘT 1: CÀI ĐẶT & ĐỒNG HỒ ---
with col_left:
    st.write("## ⚙️ Thiết lập")
    num_dice = st.radio("1. Số xúc xắc:", [1, 2], horizontal=True)
    
    if num_dice == 1:
        events = {
            "Mặt chẵn (2,4,6)": {"fn": lambda x: x[0] % 2 == 0, "theory": 3/6, "sample": "{2, 4, 6}"},
            "Mặt lẻ (1,3,5)": {"fn": lambda x: x[0] % 2 != 0, "theory": 3/6, "sample": "{1, 3, 5}"},
            "Mặt nguyên tố (2,3,5)": {"fn": lambda x: x[0] in [2,3,5], "theory": 3/6, "sample": "{2, 3, 5}"},
            "Mặt chấm > 4 (5,6)": {"fn": lambda x: x[0] > 4, "theory": 2/6, "sample": "{5, 6}"},
            "Mặt 6 chấm": {"fn": lambda x: x[0] == 6, "theory": 1/6, "sample": "{6}"}
        }
    else:
        events = {
            "Tổng bằng 7": {"fn": lambda x: sum(x) == 7, "theory": 6/36, "sample": "{(1,6), (2,5), (3,4), (4,3), (5,2), (6,1)}"},
            "Hai mặt giống nhau": {"fn": lambda x: x[0] == x[1], "theory": 6/36, "sample": "{(1,1), (2,2), (3,3), (4,4), (5,5), (6,6)}"},
            "Tổng là số chẵn": {"fn": lambda x: sum(x) % 2 == 0, "theory": 18/36, "sample": "18 kết quả chẵn"},
            "Tổng lớn hơn 9": {"fn": lambda x: sum(x) > 9, "theory": 6/36, "sample": "{(4,6), (5,5), (5,6), (6,4), (6,5), (6,6)}"}
        }
        
    selected_event_name = st.selectbox("2. Chọn biến cố:", list(events.keys()))
    num_trials = st.select_slider("3. Số lần gieo:", options=[10, 100, 500, 1000, 2000], value=100)

    st.write("---")
    st.write("## ⏱️ Thảo luận")
    timer_seconds = st.number_input("Số giây thảo luận:", min_value=5, max_value=300, value=60, step=5)
    if st.button("🔔 BẮT ĐẦU ĐẾM NGƯỢC"):
        t_placeholder = st.empty()
        for i in range(timer_seconds, -1, -1):
            mins, secs = divmod(i, 60)
            t_placeholder.markdown(f"<div class='timer-box'>{mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)
            if i == 0:
                play_sound("timer")
                st.error("⌛ Hết giờ thảo luận!")
            time.sleep(1)

# --- CỘT 2: HOẠT ĐỘNG GIEO ---
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

    placeholder.markdown("<div class='dice-container'><p style='color:#ccc;'>Sẵn sàng...</p></div>", unsafe_allow_html=True)

    if st.button("🚀 GIEO XÚC XẮC"):
        play_sound("dice")
        placeholder.markdown(f"<div class='dice-container'><img src='{urls['rolling']}' class='dice-img'></div>", unsafe_allow_html=True)
        time.sleep(1.2)
        
        results = [ (random.randint(1,6), random.randint(1,6) if num_dice==2 else None) for _ in range(num_trials) ]
        st.session_state.all_data = results
        
        last = results[-1]
        html_res = f"<div class='dice-container'><img src='{urls[last[0]]}' class='dice-img'>"
        if num_dice == 2: html_res += f"<img src='{urls[last[1]]}' class='dice-img'>"
        html_res += "</div>"
        placeholder.markdown(html_res, unsafe_allow_html=True)

    if 'all_data' in st.session_state:
        st.write("### 📊 Thống kê tần suất")
        df = pd.DataFrame(st.session_state.all_data)
        val_sum = df[0] if num_dice == 1 else df[0] + df[1]
        counts = val_sum.value_counts().sort_index().reset_index()
        counts.columns = ['Giá trị', 'Số lần']
        st.table(counts)

# --- CỘT 3: KẾT QUẢ & LÝ THUYẾT ---
with col_right:
    st.write("## 📈 Phân tích")
    ev_data = events[selected_event_name]
    
    # Hiển thị Không gian mẫu và Xác suất lý thuyết
    st.markdown(f"""
        <div class="theory-box">
            <b>📍 Không gian mẫu của biến cố (A):</b><br>
            <span style="color:#d32f2f;">A = {ev_data['sample']}</span><br><br>
            <b>🎯 Xác suất lý thuyết P(A):</b><br>
            <span style="font-size:40px; color:#1565c0;">{ev_data['theory']:.2%}</span>
        </div>
    """, unsafe_allow_html=True)

    if 'all_data' in st.session_state:
        success_count = sum(1 for r in st.session_state.all_data if ev_data['fn'](r))
        prob_exp = success_count / num_trials
        
        st.metric("XÁC SUẤT THỰC NGHIỆM P'(A)", f"{prob_exp:.2%}", delta=f"{prob_exp - ev_data['theory']:.2%} sai lệch")
        st.progress(prob_exp)
        st.write(f"👉 Xuất hiện {success_count} lần trong {num_trials} lần gieo.")
        
        st.markdown(f"""
            <div class="conclusion-box">
                <b>📌 KẾT LUẬN:</b><br>
                So sánh xác suất thực nghiệm ({prob_exp:.2%}) với lý thuyết ({ev_data['theory']:.2%}), 
                ta thấy khi số lần gieo <b>n</b> càng lớn, sự sai lệch càng giảm nhỏ!
            </div>
            """, unsafe_allow_html=True)
        # Hiển thị hình ảnh kết quả cuối cùng
        last = res[-1]
        img_tag = f"<img src='{urls[last[0]]}' class='dice-img'>"
        if num_dice == 2:
            img_tag += f"<img src='{urls[last[1]]}' class='dice-img'>"
        
        placeholder.markdown(f"<div class='dice-container'>{img_tag}</div>", unsafe_allow_html=True)

    if 'all_results' in st.session_state:
        st.write("### 📊 Thống kê tần suất")
        df_res = pd.DataFrame(st.session_state.all_results)
        v_sum = df_res[0] if num_dice == 1 else df_res[0] + df_res[1]
        counts = v_sum.value_counts().sort_index().reset_index()
        counts.columns = ['Giá trị', 'Số lần']
        st.table(counts)

# --- CỘT 3: KẾT QUẢ ---
with col_right:
    st.write("## 📈 Kết quả")
    data_ev = events[selected_name]
    
    st.markdown(f"""
        <div class="theory-box">
            <b style="color:#1e3c72;">📍 Không gian mẫu biến cố (A):</b><br>
            <span style="color:#d32f2f; font-weight:bold;">A = {data_ev['sample']}</span><br><br>
            <b style="color:#1e3c72;">🎯 Xác suất lý thuyết P(A):</b><br>
            <span style="font-size:45px; color:#1565c0; font-weight:bold;">{data_ev['theory']}</span>
        </div>
    """, unsafe_allow_html=True)

    if 'all_results' in st.session_state:
        success_num = sum(1 for r in st.session_state.all_results if data_ev['fn'](r))
        prob_exp_val = success_num / num_trials
        
        st.metric("XÁC SUẤT THỰC NGHIỆM P'(A)", f"{prob_exp_val:.2%}")
        st.progress(prob_exp_val)
        
        st.markdown(f"""
            <div class="conclusion-box">
                <b>📌 KẾT LUẬN:</b><br>
                Với n = {num_trials} lần gieo, xác suất thực nghiệm thu được là {prob_exp_val:.2%}. 
                Số lần gieo càng lớn, giá trị này càng ổn định và gần với {data_ev['t_val']:.2%}.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nhấn 'GIEO XÚC XẮC' để đối chiếu thực nghiệm!")

