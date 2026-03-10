
def trigger_marathi_alert(alert_type):
    messages = {
        "overcrowded": "सावधान! गर्दी जास्त होत आहे, सुरक्षित अंतर राखा.",
        "danger": "धोका! कृपया बाहेर जाण्याचा मार्ग वापरा.",
        "missing": "लक्ष द्या! हरवलेली व्यक्ती सापडली आहे.",
        "running": "कृपया पळू नका, शांततेत पुढे चाला."
    }
    msg = messages.get(alert_type, "सावधान!")
    
    # 🚨 थेट speak_warning फंक्शनला कॉल करा
    try:
        from voice_alert import speak_warning
        speak_warning(msg)
    except:
        pass
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import streamlit as st
import cv2
import time
import os
import requests
import numpy as np
import gc
import threading
from ultralytics import YOLO

# ==========================================
# 📁 SYSTEM DIRECTORIES & SETUP
# ==========================================
EVIDENCE_DIR = "incident_logs"
os.makedirs(EVIDENCE_DIR, exist_ok=True)

# ==========================================
# 🚨 COMMUNICATION & ALERT MODULES
# ==========================================
def send_telegram_alert(message):
    def send():
        token = "8764061611:AAGaN4wGO7ORvW-0lQbX0zkAaIAtLr37M0w"
        chat_id = "8764061611"
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        try: requests.get(url, timeout=3)
        except: pass
    threading.Thread(target=send, daemon=True).start()

def save_evidence(frame, incident_type):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{EVIDENCE_DIR}/{incident_type}_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    return filename

def log_threat(message, level="WARNING"):
    """Smart Logging System - Avoids Spam & gives Police instructions"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    color = "#FF4444" if level == "CRITICAL" else "#FFB800"
    st.session_state.threat_logs.insert(0, f"<span style='color:{color}; font-weight:bold;'>[{timestamp}] {level}:</span> {message}")
    if len(st.session_state.threat_logs) > 8:
        st.session_state.threat_logs.pop()

# ==========================================
# 🧠 TEAM CUSTOM AI MODULES IMPORTS
# ==========================================
try:
    from report_gen import create_safety_report
    from safety_math import check_proximity_violations
    from predictor import get_crowd_prediction
    from ai_brain import get_smart_alert
    from voice_alert import speak_warning 
except ImportError:
    st.warning("Running Core Independent Edge AI System.")
    def check_proximity_violations(boxes, distance_threshold): return 0
    def get_crowd_prediction(df): return "Analyzing trajectory..."
    def get_smart_alert(c, t, r): return "Crowd limit approaching", "warning"
    def speak_warning(msg): pass
    def create_safety_report(p, a): return "audit_report.pdf"

def trigger_marathi_alert(alert_type):
    messages = {
        "overcrowded": "सावधान! गर्दी जास्त होत आहे, कृपया सुरक्षित अंतर राखा आणि पोलिसांच्या सूचनांचे पालन करा.",
        "danger": "धोका! कृपया शांतता राखा आणि बाहेर जाण्याचा मार्ग वापरा. धावपळ करू नका.",
        "missing": "लक्ष द्या! हरवलेली व्यक्ती सापडली आहे.",
        "running": "कृपया पळू नका, शांततेत पुढे चाला."
    }
    msg = messages.get(alert_type, "सावधान!")
    threading.Thread(target=speak_warning, args=(msg,), daemon=True).start()

# ==========================================
# 🌌 UI & DASHBOARD CONFIGURATION
# ==========================================
st.set_page_config(page_title="Crowd Intelligence Command", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); color: #E8E8E8; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; font-weight: 700 !important; color: #FFFFFF !important; letter-spacing: -0.5px; }
    div[data-testid="metric-container"] { background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%) !important; backdrop-filter: blur(12px); border: 1px solid rgba(0, 217, 255, 0.3); border-radius: 12px; padding: 15px; box-shadow: 0 4px 15px rgba(0, 217, 255, 0.1); }
    div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; color: #00FFCC !important; font-size: 2.2rem !important; font-weight: 700 !important; }
    div[data-testid="stMetricLabel"] { color: #B8B8B8 !important; font-size: 0.9rem !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 1px;}
    .log-box { background: rgba(0,0,0,0.4); padding: 10px 12px; border-radius: 8px; border-left: 4px solid #00D9FF; font-family: 'Inter', sans-serif; font-size: 14px; margin-bottom: 8px; line-height: 1.4;}
    .ai-insight { background: rgba(0, 217, 255, 0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(0, 217, 255, 0.4); font-size: 16px; line-height: 1.6; color: #E8E8E8; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🛡️ Smart Crowd Intelligence System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00D9FF; font-size: 1.1rem; font-weight: bold;'>AI-Powered Crowd Analytics & Police Dispatch Command</p>", unsafe_allow_html=True)

# ==========================================
# 📊 DATA VISUALIZATION FUNCTIONS
# ==========================================
def create_dynamic_chart(history_df, threshold):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=history_df['Time'], y=history_df['Count'], mode='lines+markers', name='Crowd', line=dict(color='#00D9FF', width=3, shape='spline'), marker=dict(size=6, color='#FFFFFF')))
    fig.add_hrect(y0=0, y1=int(threshold * 0.7), fillcolor="rgba(0, 255, 136, 0.1)", line_width=0, annotation_text="Optimal", annotation_position="top left")
    fig.add_hrect(y0=int(threshold * 0.7), y1=threshold, fillcolor="rgba(255, 184, 0, 0.1)", line_width=0, annotation_text="Warning", annotation_position="top left")
    fig.add_hrect(y0=threshold, y1=max(threshold * 1.5, history_df['Count'].max() + 10), fillcolor="rgba(255, 68, 68, 0.1)", line_width=0, annotation_text="Danger", annotation_position="top left")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E8E8E8', family='Inter'), margin=dict(l=10, r=10, t=30, b=10), height=280, title="📈 Real-Time Trajectory")
    return fig

def create_zone_bar_chart(zones):
    fig = go.Figure(data=[go.Bar(x=list(zones.keys()), y=list(zones.values()), marker_color=['#00D9FF', '#FFB800', '#FF4444'], text=list(zones.values()), textposition='auto')])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', family='Inter'), height=280, margin=dict(l=10, r=10, t=30, b=10), title="🏛️ Spatial Distribution")
    return fig

def create_traffic_donut(total_in, total_out):
    labels = ['Entered (IN)', 'Exited (OUT)']
    values = [max(1, total_in), max(1, total_out)] 
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=['#00FF88', '#FF4444'], textinfo='label+percent')])
    fig.update_layout(title="🔄 Traffic Flow Ratio", paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=280, margin=dict(l=10, r=10, t=30, b=10), showlegend=False)
    return fig

# ==========================================
# 💾 SESSION STATE INITIALIZATION
# ==========================================
if 'history' not in st.session_state: st.session_state.history = pd.DataFrame(columns=['Time', 'Count'])
if 'peak_count' not in st.session_state: st.session_state.peak_count = 0
if 'alert_count' not in st.session_state: st.session_state.alert_count = 0
if 'tracker' not in st.session_state: st.session_state.tracker = {}
if 'heatmap_layer' not in st.session_state: st.session_state.heatmap_layer = np.zeros((480, 640), dtype=np.float32) 
if 'threat_logs' not in st.session_state: st.session_state.threat_logs = []
if 'total_in' not in st.session_state: st.session_state.total_in = 0  
if 'total_out' not in st.session_state: st.session_state.total_out = 0 
if 'ai_explanation' not in st.session_state: st.session_state.ai_explanation = "Initializing predictive models..."
if 'last_alert_time' not in st.session_state: st.session_state.last_alert_time = 0
if 'last_missing_alert' not in st.session_state: st.session_state.last_missing_alert = 0
if 'last_alert_time' not in st.session_state: st.session_state.last_alert_time = 0
st.sidebar.markdown("## ⚙️ System Configuration")


with st.sidebar.expander("📹 Camera Sources (IP/USB)", expanded=True):
    cam1_source = st.text_input("Camera 1 (Main Feed)", value="0", help="Use '0' for Webcam, or IP Cam link (e.g. http://10.164.113.180:8080/video).")
    cam2_source = st.text_input("Camera 2 (Queue Feed)", value="demo_cctv.mp4")

with st.sidebar.expander("🎛️ Engine Settings", expanded=False):
    threshold = st.slider("🚨 Maximum Crowd Capacity", 5, 200, 30)
    confidence = st.slider("🎯 AI Confidence", 0.3, 0.9, 0.45, 0.05)
    proximity_threshold = st.slider("📏 Proximity Radius (px)", 50, 200, 120)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Analytics Features")
endurance_mode = st.sidebar.toggle("⚡ Endurance Mode", False)
privacy_mode = st.sidebar.toggle("🕶️ Privacy Blur", False)
heatmap_mode = st.sidebar.toggle("🔥 Thermal Flow", False) 
line_cross_mode = st.sidebar.toggle("🚦 Bi-Directional Counter", True) 
audio_mode = st.sidebar.toggle("🔊 Marathi Voice PA", True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Missing Finder")
missing_file = st.sidebar.file_uploader("Upload Target Photo", type=['jpg', 'png'])
match_threshold = st.sidebar.slider("Match Sensitivity", 0.5, 0.9, 0.65)

target_hist = None
if missing_file:
    file_bytes = np.asarray(bytearray(missing_file.read()), dtype=np.uint8)
    target_img = cv2.imdecode(file_bytes, 1)
    st.sidebar.image(target_img, caption="Signature Extracted", width=120)
    gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
    faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(gray, 1.1, 4)
    if len(faces) > 0:
        x, y, w, h = faces[0]
        target_roi = target_img[y:y+h, x:x+w]
        target_hsv = cv2.cvtColor(target_roi, cv2.COLOR_BGR2HSV)
        target_hist = cv2.calcHist([target_hsv], [0, 1], None, [16, 16], [0, 180, 0, 256])
        cv2.normalize(target_hist, target_hist)

st.sidebar.markdown("---")
run_camera = st.sidebar.button("🔴 INITIATE SURVEILLANCE", use_container_width=True, type="primary") if not st.session_state.get('run_state', False) else st.sidebar.button("🛑 STOP SURVEILLANCE", use_container_width=True)
if run_camera:
    st.session_state['run_state'] = not st.session_state.get('run_state', False)
    st.rerun()


# 🖥️ MAIN UI LAYOUT

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
m_count = metric_col1.empty()
m_in = metric_col2.empty()
m_out = metric_col3.empty()
m_fps = metric_col4.empty()

st.markdown("---")
main_col1, main_col2 = st.columns([1.5, 1])

with main_col1:
    st.markdown("### 📹 Primary Perception Feed")
    cam1_placeholder = st.empty()
    st.markdown("### 🧠 Predictive Intelligence Briefing")
    ai_briefing_placeholder = st.empty() 

with main_col2:
    st.markdown("### 📹 Sector 2 (Queue View)")
    cam2_placeholder = st.empty()
    st.markdown("### 🚓 Police Dispatch Instructions (Logs)")
    threat_log_placeholder = st.empty() 

st.markdown("---")
g_col1, g_col2, g_col3 = st.columns([1.5, 1, 1])
with g_col1: chart_placeholder = st.empty()
with g_col2: zone_placeholder = st.empty()
with g_col3: traffic_placeholder = st.empty() 

st.markdown("---")
alert_placeholder = st.empty()

#
# 🔴 CORE INFERENCE ENGINE

if st.session_state.get('run_state', False):
    
    @st.cache_resource
    def load_model():
        try: return YOLO('models/yolov8n.pt')
        except: return YOLO('yolov8n.pt')
    
    model = load_model()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def parse_source(src):
        return int(src) if src.isdigit() else src

    cap1 = cv2.VideoCapture(parse_source(cam1_source))
    cap1.set(cv2.CAP_PROP_BUFFERSIZE, 1)  
    cap2 = cv2.VideoCapture(parse_source(cam2_source))

    frame_counter = 0
    last_chart_update = 0
    fps_start_time = time.time() 
    CROSSING_LINE_Y = 240 
    
    while st.session_state.get('run_state', False):
        current_time = time.time()
        fps = 1.0 / (current_time - fps_start_time + 1e-6)
        fps_start_time = current_time

        
        # 🛠️ CAM 1: FAIL-SAFE 'NO SIGNAL' LOGIC
       
        ret1, frame1 = cap1.read()
        
        count_people = 0
        person_boxes = []
        zones = {"Entry": 0, "Queue": 0, "Temple": 0}
        bh_alerts = []
        
        if not ret1:
            # 🚨 Camera disconnected! Show 'NO SIGNAL' instead of crashing
            annotated_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(annotated_frame, "CAM 1: NO SIGNAL", (130, 220), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            cv2.putText(annotated_frame, "Check IP Connection or Webcam", (130, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
            # Re-attempt connection in the background (helpful for IP Cams)
            if frame_counter % 60 == 0: 
                cap1 = cv2.VideoCapture(parse_source(cam1_source))
        else:
            # Normal Processing
            frame_counter += 1
            if frame_counter % (4 if endurance_mode else 2) != 0: continue 
            if endurance_mode: time.sleep(0.01) 
            if frame_counter % 150 == 0: gc.collect() 

            frame1 = cv2.resize(frame1, (640, 480))
            res1 = model.track(frame1, classes=[0], conf=confidence, persist=True, imgsz=320, verbose=False)
            annotated_frame = frame1.copy()

            if line_cross_mode:
                cv2.line(annotated_frame, (0, CROSSING_LINE_Y), (640, CROSSING_LINE_Y), (255, 0, 255), 2)
                cv2.putText(annotated_frame, "IN / ENTRY", (10, CROSSING_LINE_Y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
                cv2.putText(annotated_frame, "OUT / EXIT", (10, CROSSING_LINE_Y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

            if res1[0].boxes.id is not None:
                boxes_data = res1[0].boxes.data.cpu().numpy()
                for box in boxes_data:
                    if len(box) >= 7:
                        x1, y1, x2, y2, obj_id, conf, cls = box
                        cx, cy = int((x1+x2)/2), int((y1+y2)/2)
                        w, h = x2 - x1, y2 - y1
                        
                        if int(cls) == 0: 
                            count_people += 1
                            person_boxes.append(box)
                            
                            if cx < 213: zones["Entry"] += 1
                            elif cx < 426: zones["Queue"] += 1
                            else: zones["Temple"] += 1

                            cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                            
                            if obj_id in st.session_state.tracker:
                                prev_cx, prev_cy, prev_time = st.session_state.tracker[obj_id]
                                
                                if line_cross_mode:
                                    if prev_cy < CROSSING_LINE_Y and cy >= CROSSING_LINE_Y:
                                        st.session_state.total_in += 1
                                    elif prev_cy > CROSSING_LINE_Y and cy <= CROSSING_LINE_Y:
                                        st.session_state.total_out += 1

                                dist = ((cx-prev_cx)**2 + (cy-prev_cy)**2)**0.5
                                if dist / (current_time - prev_time + 1e-6) > 400: 
                                    bh_alerts.append("PANIC / RUNNING DETECTED")
                            
                            if w > h * 1.5: bh_alerts.append("PERSON FALLEN")
                            st.session_state.tracker[obj_id] = (cx, cy, current_time)

                            if heatmap_mode: cv2.circle(st.session_state.heatmap_layer, (cx, cy), 20, 3, -1)
                        
            cv2.line(annotated_frame, (213, 0), (213, 480), (0, 255, 255), 1, cv2.LINE_AA)
            cv2.line(annotated_frame, (426, 0), (426, 480), (0, 255, 255), 1, cv2.LINE_AA)
            cv2.rectangle(annotated_frame, (0, 0), (640, 35), (0,0,0), -1)
            cv2.putText(annotated_frame, f"E:{zones['Entry']} | Q:{zones['Queue']} | T:{zones['Temple']}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            if heatmap_mode:
                st.session_state.heatmap_layer = np.clip(st.session_state.heatmap_layer - 0.5, 0, 255)
                heatmap_color = cv2.applyColorMap(st.session_state.heatmap_layer.astype(np.uint8), cv2.COLORMAP_JET)
                mask = st.session_state.heatmap_layer > 5
                mask_3c = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
                annotated_frame = np.where(mask_3c, cv2.addWeighted(annotated_frame, 0.6, heatmap_color, 0.4, 0), annotated_frame)

            if privacy_mode:
                gray_for_blur = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
                privacy_faces = face_cascade.detectMultiScale(gray_for_blur, 1.1, 4)
                for (px, py, pw, ph) in privacy_faces:
                    px, py = max(0, px), max(0, py)
                    pw, ph = min(640 - px, pw), min(480 - py, ph)
                    if annotated_frame[py:py+ph, px:px+pw].size > 0:
                        annotated_frame[py:py+ph, px:px+pw] = cv2.GaussianBlur(annotated_frame[py:py+ph, px:px+pw], (51, 51), 0)

           # 👤 MISSING PERSON RADAR (OPTIMIZED)
        if target_hist is not None and frame_counter % 4 == 0:
            gray_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            current_faces = face_cascade.detectMultiScale(gray_frame, 1.1, 5, minSize=(40, 40))
            
            for (fx, fy, fw, fh) in current_faces:
                # चेहरा सापडला की निळा बॉक्स
                cv2.rectangle(annotated_frame, (fx, fy), (fx+fw, fy+fh), (255, 0, 0), 2)
                
                current_roi = frame1[fy:fy+fh, fx:fx+fw]
                current_hsv = cv2.cvtColor(current_roi, cv2.COLOR_BGR2HSV)
                current_hist = cv2.calcHist([current_hsv], [0, 1], None, [16, 16], [0, 180, 0, 256])
                cv2.normalize(current_hist, current_hist)
                
                # 🧠 AI Comparison
                score = cv2.compareHist(target_hist, current_hist, cv2.HISTCMP_CORREL)
                
                # जर स्कोर Sensitivity पेक्षा जास्त असेल (उदा. 0.65)
                if score > match_threshold:
                    cv2.rectangle(annotated_frame, (fx, fy), (fx+fw, fy+fh), (0, 0, 255), 4)
                    
                    # 🚨 CHECK COOLDOWN (सारखा आवाज येऊ नये म्हणून १५ सेकंदाचा गॅप)
                    if (current_time - st.session_state.last_missing_alert) > 15:
                        
                        # १. टेलिग्राम आणि लॉग्ज
                        log_msg = f"📢 DISPATCH: Missing Person matched ({int(score*100)}%)."
                        log_threat(log_msg, "CRITICAL")
                        send_telegram_alert(f"🚨 {log_msg}")
                        
                        # २. 🔊 MARATHI VOICE (Direct Trigger)
                        if audio_mode:
                            # आपण थेट voice_alert मधलं फंक्शन कॉल करूया थ्रेडिंग सोडून
                            try:
                                # थेट मराठी मेसेज पाठवा
                                speak_warning("लक्ष द्या! हरवलेली व्यक्ती सापडली आहे.") 
                            except Exception as e:
                                # जर वरील ओळ एरर देत असेल तर हे वापर:
                                trigger_marathi_alert("missing")
                        
                        # ३. फोटो सेव्ह आणि टोस्ट
                        save_evidence(annotated_frame, "MISSING_PERSON")
                        st.session_state.last_missing_alert = current_time
                        st.toast("🚨 Missing Person Identified!", icon="👤")

            cv2.putText(annotated_frame, f"FPS: {int(fps)}", (550, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
        # Display Cam 1 (Either Normal Frame or NO SIGNAL Frame)
        cam1_placeholder.image(annotated_frame, channels="BGR", use_container_width=True)
        
       
        # 🛠️ CAM 2: FAIL-SAFE 'NO SIGNAL' LOGIC

        if cap2.isOpened():
            ret2, frame2 = cap2.read()
            if not ret2 and not str(cam2_source).isdigit(): 
                cap2.set(cv2.CAP_PROP_POS_FRAMES, 0); ret2, frame2 = cap2.read()
            
            if ret2:
                frame2 = cv2.resize(frame2, (640, 480))
                if frame_counter % (6 if endurance_mode else 3) == 0: 
                    res2 = model.track(frame2, classes=[0], conf=confidence, persist=True, imgsz=320, verbose=False)
                    f2_out = res2[0].plot()
                else: f2_out = frame2 
                cv2.putText(f2_out, f"CCTV 2: {cam2_source}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cam2_placeholder.image(f2_out, channels="BGR", use_container_width=True)
            else:
                error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(error_frame, f"CCTV 2: OFFLINE", (150, 220), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
                cam2_placeholder.image(error_frame, channels="BGR", use_container_width=True)
                if frame_counter % 60 == 0: cap2 = cv2.VideoCapture(parse_source(cam2_source))
        else:
            error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(error_frame, f"CCTV 2: OFFLINE", (150, 220), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
            cam2_placeholder.image(error_frame, channels="BGR", use_container_width=True)

        # 🧠 EXPLAINABLE AI LOGIC
        if frame_counter % 30 == 0 and ret1: # Only predict if Cam 1 is alive
            if len(st.session_state.history) > 5:
                past_count = st.session_state.history['Count'].iloc[-5]
                trend_diff = count_people - past_count
                base_pred = get_crowd_prediction(st.session_state.history) 
                if trend_diff >= 3:
                    st.session_state.ai_explanation = f"⚠️ **Critical Alert:** Crowd inflow velocity is high (<b>+{trend_diff} persons</b>). Threshold ({threshold}) breach expected shortly. <br>🛡️ **Action:** Deploy staff to Entry Zone to throttle flow."
                elif trend_diff <= -2:
                    st.session_state.ai_explanation = f"📉 **Status Nominal:** Crowd is naturally dispersing. Flow is stabilizing. <br>🛡️ **Action:** No immediate action required."
                else:
                    st.session_state.ai_explanation = f"✅ **Status Stable:** Volumetric density is currently balanced. <br>🛡️ **Action:** Standard monitoring protocol."
        elif not ret1:
            st.session_state.ai_explanation = "❌ **System Offline:** Awaiting video signal restoration to resume analytics."

        ai_briefing_placeholder.markdown(f"<div class='ai-insight'>{st.session_state.ai_explanation}</div>", unsafe_allow_html=True)

        st.session_state.peak_count = max(st.session_state.peak_count, count_people)
        m_count.metric("👥 Active Trajectory", count_people, delta=f"{count_people - threshold} capacity", delta_color="inverse")
        m_in.metric("🟢 Total Entered (IN)", st.session_state.total_in)
        m_out.metric("🔴 Total Exited (OUT)", st.session_state.total_out)
        m_fps.metric("⚡ Logic Core FPS", int(fps) if ret1 else 0)

        logs_html = "".join([f"<div class='log-box'>{l}</div>" for l in st.session_state.threat_logs])
        threat_log_placeholder.markdown(logs_html if logs_html else "<p style='color:gray; font-family:monospace;'>[System] Listening for anomalies...</p>", unsafe_allow_html=True)

        if current_time - last_chart_update > 1.2:
            now = datetime.now().strftime("%H:%M:%S")
            st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame({'Time': [now], 'Count': [count_people]})]).tail(20)
            chart_placeholder.plotly_chart(create_dynamic_chart(st.session_state.history, threshold), use_container_width=True, key=f"trend_{frame_counter}")
            zone_placeholder.plotly_chart(create_zone_bar_chart(zones), use_container_width=True, key=f"zone_{frame_counter}")
            traffic_placeholder.plotly_chart(create_traffic_donut(st.session_state.total_in, st.session_state.total_out), use_container_width=True, key=f"donut_{frame_counter}")
            last_chart_update = current_time
        
        # 🚨 ACTIONABLE POLICE DISPATCH LOGIC (Anti-Spam)
        if bh_alerts and (current_time - st.session_state.last_alert_time) > 10:
            dispatch_msg = f"📢 DISPATCH: Panic Running detected. Send Quick Response Team (QRT) to Sector A."
            alert_placeholder.error(f"🚨 **CRITICAL BEHAVIOR:** {dispatch_msg}")
            log_threat(dispatch_msg, "CRITICAL")
            send_telegram_alert(f"URGENT: {dispatch_msg}")
            if audio_mode: trigger_marathi_alert("running")
            st.session_state.last_alert_time = current_time
            
        elif count_people > threshold and (current_time - st.session_state.last_alert_time) > 20: 
            st.session_state.alert_count += 1
            dispatch_msg = f"📢 DISPATCH: Capacity breached ({count_people}/{threshold}). Halt inflow & open emergency Exit B."
            log_threat(dispatch_msg, "WARNING")
            send_telegram_alert(f"⚠️ Crowd Warning: {dispatch_msg}")
            if audio_mode: trigger_marathi_alert("overcrowded")
            st.session_state.last_alert_time = current_time

    if cap1 is not None: cap1.release()
    if cap2 is not None: cap2.release()

#
# 📄 POST-MISSION EXPORT & EVIDENCE
# 
st.sidebar.markdown("---")
st.sidebar.markdown("### 📂 Command Archives")
if not st.session_state.get('run_state', False):
    with st.sidebar.expander("📸 Incident Gallery Viewer", expanded=False):
        logs = [f for f in os.listdir(EVIDENCE_DIR) if f.endswith('.jpg')] if os.path.exists(EVIDENCE_DIR) else []
        if logs:
            st.write(f"Found {len(logs)} high-res evidences.")
            for log_file in sorted(logs, reverse=True)[:3]: st.image(f"{EVIDENCE_DIR}/{log_file}", caption=log_file)
        else: st.write("Archive clean. No incidents.")

    if not st.session_state.history.empty:
        csv_data = st.session_state.history.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button("💾 Download Telemetry (CSV)", data=csv_data, file_name=f"crowd_telemetry_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)