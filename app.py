import pandas as pd
from datetime import datetime
import streamlit as st
import cv2
from ultralytics import YOLO
import time
import os

# --- Team Modules Import ---
from report_gen import create_safety_report
from safety_math import check_proximity_violations
from predictor import get_crowd_prediction
from ai_brain import get_smart_alert
from voice_alert import speak_warning  # 🔊 Voice Alert Module

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

# Initialize data history
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Time', 'Count'])

# Load YOLOv8
@st.cache_resource
def load_model():
    return YOLO('models/yolov8n.pt')
model = load_model()

# 3. Sidebar Configuration
st.sidebar.header("🎛️ Control Panel")
threshold = st.sidebar.slider("Crowd Limit", 5, 50, 10)
run_camera = st.sidebar.toggle("🔴 Start Dual Surveillance")

# 4. Top Row (Metrics)
st.markdown("### 📊 Live Network Analytics")
metric_col1, metric_col2, metric_col3 = st.columns(3)
count_metric = metric_col1.empty()
risk_metric = metric_col2.empty()
trend_metric = metric_col3.empty()

# 5. Dual Camera Layout
st.markdown("---")
cam1_col, cam2_col = st.columns(2)
with cam1_col:
    st.markdown("<h4>📷 Cam 1: Main Gate (Webcam)</h4>", unsafe_allow_html=True)
    cam1_placeholder = st.empty()
with cam2_col:
    st.markdown("<h4>📱 Cam 2: VIP Zone (Phone)</h4>", unsafe_allow_html=True)
    cam2_placeholder = st.empty()

st.markdown("---")

# 6. Chart & Alerts Layout
chart_col, alert_col = st.columns([2, 1])
with chart_col:
    st.markdown("<h4>📈 Network Trend</h4>", unsafe_allow_html=True)
    chart_placeholder = st.empty()
with alert_col:
    st.markdown("<h4>🚨 Central Alerts</h4>", unsafe_allow_html=True)
    alert_placeholder = st.empty()

# ---------------------------------------------------------
# 🔴 Main Loop: Running 2 Cameras
# ---------------------------------------------------------
if run_camera:
    # ⚠️ महत्त्वाची टीप: इथे तुझ्या फोनवर दिसणारा IP Address टाक
    phone_ip = "http://192.168.137.95:8080/video" 
    
    cap1 = cv2.VideoCapture(0)         
    cap2 = cv2.VideoCapture(phone_ip)  
    
    frame_counter = 0 # 🟢 Lag Fix Counter
    
    while cap1.isOpened() and cap2.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        
        if not ret1 or not ret2: 
            st.error("⚠️ Connection Lost! Please check WiFi or Camera.")
            break
            
        frame_counter += 1
        
        # 🟢 FIX: Process only every 3rd frame to stop LAG!
        if frame_counter % 3 != 0:
            continue
        
        # 🟢 FIX: Resize both frames so they fit perfectly
        frame1 = cv2.resize(frame1, (640, 480))
        frame2 = cv2.resize(frame2, (640, 480))
            
        # 🟢 ULTIMATE SPEED FIX: imgsz=320 
        # Cam 1 Processing
        res1 = model(frame1, classes=[0], conf=0.5, imgsz=320, verbose=False)
        count1 = len(res1[0].boxes)
        cam1_placeholder.image(res1[0].plot(), channels="BGR")
        
        # Cam 2 Processing
        res2 = model(frame2, classes=[0], conf=0.5, imgsz=320, verbose=False)
        count2 = len(res2[0].boxes)
        cam2_placeholder.image(res2[0].plot(), channels="BGR")
        
        # Total People Logic
        current_count = count1 + count2
        
        # Proximity Logic (Checking Cam 1)
        boxes1 = res1[0].boxes.xyxy.cpu().numpy()
        risky_people = check_proximity_violations(boxes1, distance_threshold=150)
        
        count_metric.metric("Total People (Network)", current_count)
        risk_metric.metric("⚠️ High Risk", risky_people)
        
        prediction_text = get_crowd_prediction(st.session_state.history)
        trend_metric.metric("🔮 Future Trend", prediction_text)
        
        now = datetime.now().strftime("%H:%M:%S")
        new_row = pd.DataFrame({'Time': [now], 'Count': [current_count]})
        st.session_state.history = pd.concat([st.session_state.history, new_row]).tail(20)
        chart_placeholder.line_chart(st.session_state.history.set_index('Time'))
        
        # AI Brain Alerts & Voice
        if 'last_alert_time' not in st.session_state:
            st.session_state.last_alert_time = 0

        current_time_sec = time.time()
        
        if current_count > threshold or risky_people > 2:
            if (current_time_sec - st.session_state.last_alert_time) > 15:
                msg, status = get_smart_alert(current_count, threshold, risky_people)
                st.session_state.last_alert_msg = msg
                st.session_state.last_alert_status = status
                st.session_state.last_alert_time = current_time_sec
                
                # 🔊 NEW: Marathi Audio Warning
                if status == "danger":
                    speak_warning("Attention! Krupaya laksha dya. Gardi limit peksha jaast zali aahe. Krupaya surakshit antar theva.")
                else:
                    speak_warning("Alert. Gardi vaadhat aahe. Krupaya niyam che palan kara.")
            
            if 'last_alert_msg' in st.session_state:
                if st.session_state.last_alert_status == "danger":
                    alert_placeholder.error(st.session_state.last_alert_msg)
                else:
                    alert_placeholder.warning(st.session_state.last_alert_msg)
        else:
            alert_placeholder.success("✅ Network Secure. All zones normal.")
            
        if not run_camera: 
            break
            
    cap1.release()
    cap2.release()

# ---------------------------------------------------------
# 7. 📄 PDF Safety Report Generator (Sidebar)
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color:#00FFCC;'>📄 Safety Report</h3>", unsafe_allow_html=True)

if run_camera:
    st.sidebar.warning("⚠️ Turn OFF 'Start Surveillance' to download the report.")
else:
    if st.sidebar.button("⚙️ Generate PDF Report"):
        try:
            peak_crowd = int(st.session_state.history['Count'].max()) if not st.session_state.history.empty else 0
            pdf_filename = create_safety_report(max_crowd=peak_crowd, alerts_triggered=len(st.session_state.history))
            
            with open(pdf_filename, "rb") as pdf_file:
                st.sidebar.download_button(
                    label="📥 Download Daily Report",
                    data=pdf_file,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )
            st.sidebar.success("✅ Report Generated!")
        except Exception as e:
            st.sidebar.error(f"Error generating report: {e}")