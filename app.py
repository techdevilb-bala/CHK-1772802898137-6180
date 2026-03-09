import pandas as pd
from predictor import get_crowd_prediction
from datetime import datetime
import streamlit as st
import cv2
from ultralytics import YOLO
import time
import os

# --- Team Modules Import ---
from report_gen import create_safety_report
from safety_math import check_proximity_violations
from ai_brain import get_smart_alert  # 🧠 3-Tier Master Brain
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
from ai_brain import get_smart_alert  # 🧠 3-Tier Master Brain

# 1. Page Config
st.set_page_config(page_title="Smart Crowd Intelligence", layout="wide", initial_sidebar_state="expanded")

# 2. 🚀 CHAKRAVYUH 2.0 CYBERPUNK UI THEME
st.markdown("""
    <style>
    /* Import Futuristic Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');

    /* Main Background - Deep Space / Cyberpunk */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(10, 10, 18) 0%, rgb(0, 0, 0) 90%);
        color: #E0E0E0;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Big Titles with Gradient & Glow */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        background: -webkit-linear-gradient(45deg, #00F0FF, #7000FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 15px rgba(0, 240, 255, 0.4);
        text-align: center;
    }

    /* Glassmorphism Metrics Boxes (The 3 boxes at top) */
    div[data-testid="metric-container"] {
        background: rgba(20, 20, 35, 0.6) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 240, 255, 0.3);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 240, 255, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    /* Hover effect on metrics - Bounces up & glows */
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 32px 0 rgba(0, 240, 255, 0.4);
        border: 1px solid rgba(0, 240, 255, 0.8);
    }

    /* Glowing Numbers inside metrics */
    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif !important;
        color: #00FFCC !important;
        text-shadow: 0px 0px 10px rgba(0, 255, 204, 0.5);
    }

    /* Camera Border with Purple Glow */
    div[data-testid="stImage"] > img {
        border: 2px solid #7000FF;
        border-radius: 10px;
        box-shadow: 0px 0px 20px rgba(112, 0, 255, 0.4);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 10, 15, 0.95) !important;
        border-right: 1px solid rgba(112, 0, 255, 0.3);
    }
    
    /* Button Styling */
    button {
        border: 1px solid #00F0FF !important;
        color: #00F0FF !important;
        border-radius: 5px !important;
        transition: all 0.3s ease !important;
    }
    button:hover {
        background: rgba(0, 240, 255, 0.1) !important;
        box-shadow: 0px 0px 15px rgba(0, 240, 255, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)
# Initialize data history
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Time', 'Count'])

# Load YOLOv8
@st.cache_resource
def load_model():
    return YOLO('models/yolov8n.pt')
model = load_model()

# 3. Sidebar Configuration (Only Controls)
st.sidebar.header("🎛️ Control Panel")
threshold = st.sidebar.slider("Crowd Limit", 5, 50, 10)
run_camera = st.sidebar.toggle("🔴 Start Surveillance")

# 4. MAIN DASHBOARD LAYOUT (Top Row: 3 Metrics)
st.markdown("### 📊 Live Analytics")
metric_col1, metric_col2, metric_col3 = st.columns(3)
count_metric = metric_col1.empty()
risk_metric = metric_col2.empty()
trend_metric = metric_col3.empty()

st.markdown("---")

# 5. Middle Row (Camera on Left, Chart on Right)
cam_col, chart_col = st.columns([2, 1])
with cam_col:
    st.markdown("#### 📷 Live Camera Feed")
    frame_placeholder = st.empty()
with chart_col:
    st.markdown("#### 📈 Crowd Trend")
    chart_placeholder = st.empty()
    st.markdown("#### 🚨 Alerts")
    alert_placeholder = st.empty()

# ---------------------------------------------------------
# यानंतर तुझा जुना 'if run_camera:' आणि while loop चा कोड तसाच राहील.
if run_camera:
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: 
            st.error("Camera access failed!")
            break
        
        # AI Detection
        results = model(frame, classes=[0], conf=0.5, verbose=False)
        current_count = len(results[0].boxes)
        
        # Proximity Math
        boxes = results[0].boxes.xyxy.cpu().numpy()
        risky_people = check_proximity_violations(boxes, distance_threshold=150)
        
        # Update chart data
        now = datetime.now().strftime("%H:%M:%S")
        new_row = pd.DataFrame({'Time': [now], 'Count': [current_count]})
        st.session_state.history = pd.concat([st.session_state.history, new_row]).tail(20)
        
        # Display Results
        chart_placeholder.line_chart(st.session_state.history.set_index('Time'))
        frame_placeholder.image(results[0].plot(), channels="BGR")
        
        # Update Dashboard Metrics
     
# Update Dashboard Metrics
        count_metric.metric("Total People", current_count)
        risk_metric.metric("⚠️ High Risk", risky_people)
        
        # --- NEW: Predictive Analytics ---
        prediction_text = get_crowd_prediction(st.session_state.history)
        trend_metric.metric("🔮 Future Trend", prediction_text)
        # ---------------------------------------------------------
        # 🧠 3-Tier AI Brain Integration (With 15s Cooldown)
        # ---------------------------------------------------------
        if 'last_alert_time' not in st.session_state:
            st.session_state.last_alert_time = 0

        current_time_sec = time.time()
        
        if current_count > threshold or risky_people > 2:
            # 15 seconds cooldown
            if (current_time_sec - st.session_state.last_alert_time) > 15:
                msg, status = get_smart_alert(current_count, threshold, risky_people)
                
                st.session_state.last_alert_msg = msg
                st.session_state.last_alert_status = status
                st.session_state.last_alert_time = current_time_sec
            
            # Show the saved alert message
            if 'last_alert_msg' in st.session_state:
                if st.session_state.last_alert_status == "danger":
                    alert_placeholder.error(st.session_state.last_alert_msg)
                else:
                    alert_placeholder.warning(st.session_state.last_alert_msg)
        else:
            alert_placeholder.success("✅ Crowd is within safe limits. Proper distancing maintained.")
        # ---------------------------------------------------------

        if not run_camera: 
            break
    
    cap.release()

# --- NEW: PDF Report Generator (Safe Mode) ---
st.sidebar.markdown("---")
st.sidebar.subheader("📄 Daily Safety Report")

if run_camera:
    st.sidebar.warning("⚠️ Turn OFF 'Start Surveillance' to download the report.")
else:
    if st.sidebar.button("1. Generate Report"):
        try:
            peak_crowd = int(st.session_state.history['Count'].max()) if not st.session_state.history.empty else 0
            pdf_filename = create_safety_report(max_crowd=peak_crowd, alerts_triggered=len(st.session_state.history))
            
            st.session_state['generated_pdf'] = pdf_filename
            st.sidebar.success("✅ Report Ready!")
        except Exception as e:
            st.sidebar.error(f"Error generating report: {e}")

    if 'generated_pdf' in st.session_state:
        try:
            with open(st.session_state['generated_pdf'], "rb") as pdf_file:
                st.sidebar.download_button(
                    label="2. ⬇️ Download PDF",
                    data=pdf_file,
                    file_name=st.session_state['generated_pdf'],
                    mime="application/pdf"
                )
        except FileNotFoundError:
            st.sidebar.error("File not found. Please click Generate again.")