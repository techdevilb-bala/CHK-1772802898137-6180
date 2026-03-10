import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import streamlit as st
import cv2
from ultralytics import YOLO
import time
import os
import requests 

# --- Team Modules Import ---
from report_gen import create_safety_report
from safety_math import check_proximity_violations
from predictor import get_crowd_prediction
from ai_brain import get_smart_alert
from voice_alert import speak_warning 

# 1. Page Config & Cyberpunk UI
st.set_page_config(page_title="Smart Crowd Intelligence", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    .stApp { background: radial-gradient(circle at 10% 20%, rgb(10, 10, 18) 0%, rgb(0, 0, 0) 90%); color: #E0E0E0; font-family: 'Rajdhani', sans-serif; }
    h1, h2, h3, h4 { font-family: 'Orbitron', sans-serif !important; background: -webkit-linear-gradient(45deg, #00F0FF, #7000FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0px 0px 15px rgba(0, 240, 255, 0.4); text-align: center; }
    div[data-testid="metric-container"] { background: rgba(20, 20, 35, 0.6) !important; backdrop-filter: blur(10px); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 12px; padding: 15px; box-shadow: 0 8px 32px 0 rgba(0, 240, 255, 0.1); }
    div[data-testid="stMetricValue"] { font-family: 'Orbitron', sans-serif !important; color: #00FFCC !important; text-shadow: 0px 0px 10px rgba(0, 255, 204, 0.5); }
    div[data-testid="stImage"] > img { border: 2px solid #7000FF; border-radius: 10px; box-shadow: 0px 0px 20px rgba(112, 0, 255, 0.4); }
    section[data-testid="stSidebar"] { background-color: rgba(10, 10, 15, 0.95) !important; border-right: 1px solid rgba(112, 0, 255, 0.3); }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2>🛡️ SMART CROWD SURVEILLANCE</h2>", unsafe_allow_html=True)

# --- 📊 Dynamic Risk Chart Function (Fixed glow-dot) ---
def create_dynamic_chart(history_df, threshold):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=history_df['Time'], y=history_df['Count'],
        mode='lines+markers', name='Live Count',
        line=dict(color='#00F0FF', width=3, shape='spline'),
        marker=dict(size=8, color='#7000FF', symbol='circle-dot'), # 🟢 Fixed Symbol
        fill='tozeroy', fillcolor='rgba(0, 240, 255, 0.1)'
    ))
    # Threshold Lines
    fig.add_hline(y=int(threshold * 0.7), line_dash="dash", line_color="#FFFF00", annotation_text="🟡 Warning")
    fig.add_hline(y=threshold, line_dash="dash", line_color="#FF2A2A", annotation_text="🔴 Danger")
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0E0E0'), margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    return fig

# Initialize History
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Time', 'Count'])

# Load YOLO
@st.cache_resource
def load_model():
    return YOLO('models/yolov8n.pt')
model = load_model()

# Sidebar Control
st.sidebar.header("🎛️ Control Panel")
threshold = st.sidebar.slider("Crowd Limit", 5, 100, 15)
run_camera = st.sidebar.toggle("🔴 Start Dual Surveillance")

# Metrics
st.markdown("### 📊 Live Analytics")
metric_col1, metric_col2, metric_col3 = st.columns(3)
count_metric = metric_col1.empty()
risk_metric = metric_col2.empty()
trend_metric = metric_col3.empty()

# Camera Layout
st.markdown("---")
cam1_col, cam2_col = st.columns(2)
cam1_placeholder = cam1_col.empty()
cam2_placeholder = cam2_col.empty()

chart_col, alert_col = st.columns([2, 1])
chart_placeholder = chart_col.empty()
alert_placeholder = alert_col.empty()

# ---------------------------------------------------------
# 🔴 Main Loop: Stable Hybrid Mode
# ---------------------------------------------------------
if run_camera:
    phone_ip = "http://192.168.137.95:8080/video" 
    
    cap1 = cv2.VideoCapture(0)         
    cap2 = None
    
    # 📱 Safe Phone Check
    try:
        check_ip = phone_ip.replace("/video", "/status.json")
        response = requests.get(check_ip, timeout=1.2)
        if response.status_code == 200:
            cap2 = cv2.VideoCapture(phone_ip)
            st.sidebar.success("✅ Phone Connected")
    except:
        st.sidebar.info("📱 Phone Offline. Running on Webcam.")

    frame_counter = 0 
    
    while run_camera:
        ret1, frame1 = cap1.read()
        ret2 = False
        if cap2 and cap2.isOpened():
            ret2, frame2 = cap2.read()
            
        if not ret1 and not ret2:
            st.error("No active cameras found!")
            break
            
        frame_counter += 1
        if frame_counter % 3 != 0: continue

        # --- 🧠 Process Cam 1 ---
        if ret1:
            frame1 = cv2.resize(frame1, (640, 480))
            res1 = model(frame1, classes=[0], conf=0.4, imgsz=320, verbose=False)
            count1 = len(res1[0].boxes)
            cam1_placeholder.image(res1[0].plot(), channels="BGR")
            boxes1 = res1[0].boxes.xyxy.cpu().numpy()
            risky_people = check_proximity_violations(boxes1, distance_threshold=150)
        else:
            cam1_placeholder.warning("📷 Cam 1 Offline")
            count1, risky_people = 0, 0

        # --- 🧠 Process Cam 2 ---
        if ret2:
            frame2 = cv2.resize(frame2, (640, 480))
            res2 = model(frame2, classes=[0], conf=0.4, imgsz=320, verbose=False)
            count2 = len(res2[0].boxes)
            cam2_placeholder.image(res2[0].plot(), channels="BGR")
        else:
            cam2_placeholder.info("📱 Cam 2 (Phone) Offline")
            count2 = 0

        # --- 📊 Unified Analytics ---
        total_count = count1 + count2
        count_metric.metric("Total People", total_count)
        risk_metric.metric("⚠️ High Risk", risky_people)
        
        prediction = get_crowd_prediction(st.session_state.history)
        trend_metric.metric("🔮 Future Trend", prediction)
        
        # Trend Update
        now = datetime.now().strftime("%H:%M:%S")
        new_entry = pd.DataFrame({'Time': [now], 'Count': [total_count]})
        st.session_state.history = pd.concat([st.session_state.history, new_entry]).tail(30)
        
        if frame_counter % 6 == 0:
            fig = create_dynamic_chart(st.session_state.history, threshold)
            chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        # --- 🚨 AI Alerts & Voice ---
        if 'last_alert_time' not in st.session_state: st.session_state.last_alert_time = 0
        
        if total_count > threshold or risky_people > 3:
            if (time.time() - st.session_state.last_alert_time) > 20:
                msg, status = get_smart_alert(total_count, threshold, risky_people) # 🟢 Using total_count
                st.session_state.last_alert_msg = msg
                st.session_state.last_alert_status = status
                st.session_state.last_alert_time = time.time()
                speak_warning("Krupaya laksha dya. Gardi limit peksha jaast zali aahe.")
            
            if 'last_alert_msg' in st.session_state:
                if st.session_state.last_alert_status == "danger": alert_placeholder.error(st.session_state.last_alert_msg)
                else: alert_placeholder.warning(st.session_state.last_alert_msg)
        else:
            alert_placeholder.success("✅ System Status: Secure")

    cap1.release()
    if cap2: cap2.release()

# 📄 PDF Sidebar
st.sidebar.markdown("---")
if not run_camera:
    if st.sidebar.button("📊 Generate PDF Report"):
        peak_c = int(st.session_state.history['Count'].max()) if not st.session_state.history.empty else 0
        pdf_path = create_safety_report(peak_c, len(st.session_state.history))
        with open(pdf_path, "rb") as f:
            st.sidebar.download_button("📥 Download Official Report", f, file_name=pdf_path)