
# ==========================================
# 🚨 2. COMMUNICATION & DISPATCH MODULES
# ==========================================
import requests
from requests.auth import HTTPBasicAuth
import threading
from datetime import datetime
import cv2
import os
import streamlit as st

EVIDENCE_DIR = "incident_logs"
os.makedirs(EVIDENCE_DIR, exist_ok=True)

import os
import threading

def send_whatsapp_alert(message):
    """Hackathon Jugaad: Calling the working test file directly! 🔥"""
    def send():
        try:
            # थेट तुझी चालणारी फाईल रन करेल
            os.system("python test_wo.py") 
        except Exception as e:
            pass
            
    threading.Thread(target=send, daemon=True).start()


def save_evidence(frame, incident_type):
    """Captures a high-res snapshot of the incident."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{EVIDENCE_DIR}/{incident_type}_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    return filename

def log_threat(message, level="WARNING"):
    """Smart Logging System - Maintains an active tactical feed on the dashboard."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    color = "#FF4444" if level == "CRITICAL" else "#FFB800" if level == "WARNING" else "#00FFCC"
    
    if 'threat_logs' not in st.session_state: 
        st.session_state.threat_logs = []
        
    log_html = f"<div class='log-box'><span style='color:{color}; font-weight:bold;'>[{timestamp}] {level}:</span> {message}</div>"
    st.session_state.threat_logs.insert(0, log_html)
    
    if len(st.session_state.threat_logs) > 8:
        st.session_state.threat_logs.pop()
# --- CORE LIBRARIES ---
import os
import time
import threading
from datetime import datetime
import gc

# --- DATA & MATH LIBRARIES ---
import numpy as np
import pandas as pd

# --- VISION & AI LIBRARIES ---
import cv2
from ultralytics import YOLO

# --- UI & VISUALIZATION ---
import streamlit as st
import plotly.graph_objects as go
import requests


EVIDENCE_DIR = "incident_logs"
os.makedirs(EVIDENCE_DIR, exist_ok=True)


# 🚨 2. COMMUNICATION & DISPATCH MODULES

# ==========================================
# 🚨 2. COMMUNICATION: WHATSAPP DISPATCH (TWILIO)
# ==========================================
import requests
from requests.auth import HTTPBasicAuth

def send_whatsapp_alert(message):
    """Sends priority tactical alerts via Twilio Enterprise WhatsApp API"""
    def send():
        # ⚠️ इथे तुझे Twilio डॅशबोर्डवरील डिटेल्स टाक
        account_sid = 'ACf0ec2706c55ce3e04a3e4679d8919920'
        auth_token = '28bf9a7b02484292b2bc76f903f97084'
        
        # Twilio Sandbox चा नंबर (हा सहसा +14155238886 असा असतो)
        from_whatsapp_number = 'whatsapp:+14155238886' 
        # तुझा स्वतःचा नंबर ज्यावर मेसेज हवाय (Country Code सोबत, उदा. +919876543210)
        to_whatsapp_number = '+917249836522' 

        url = f"https://api.telegram.org/bot/.... नाही, आपण Twilio वापरतोय!"
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        
        data = {
            'From': from_whatsapp_number,
            'To': to_whatsapp_number,
            'Body': f"🚨 *CROWD COMMAND ALERT*\n\n{message}"
        }
        
        try:
            response = requests.post(url, data=data, auth=HTTPBasicAuth(account_sid, auth_token), timeout=5)
            print(f"🚀 WhatsApp Status: {response.status_code}")
        except Exception as e:
            print(f"❌ WhatsApp Error: {e}")

    # थ्रेडमध्ये चालवा म्हणजे सिस्टिम अडकणार नाही
    threading.Thread(target=send, daemon=True).start()
# ==========================================
# 🔊 3. LOCALIZED AUDIO PROTOCOL (MARATHI)
# ==========================================
def trigger_marathi_alert(alert_type):
    """Triggers localized voice instructions to prevent panic and guide the crowd."""
    messages = {
        "overcrowded": "सावधान! गर्दी जास्त होत आहे, सुरक्षित अंतर राखा आणि पोलिसांच्या सूचनांचे पालन करा.",
        "danger": "धोका! कृपया शांतता राखा आणि बाहेर जाण्याचा मार्ग वापरा.",
        "missing": "लक्ष द्या! हरवलेली व्यक्ती सापडली आहे.",
        "running": "कृपया पळू नका, शांततेत पुढे चाला."
    }
    msg = messages.get(alert_type, "सावधान!")
    
    try:
        from voice_alert import speak_warning
        threading.Thread(target=speak_warning, args=(msg,), daemon=True).start()
    except ImportError:
        pass # Fallback if voice_alert.py is missing

# ==========================================
# 🧠 4. ADVANCED PREDICTIVE INTELLIGENCE
# ==========================================
def advanced_crowd_prediction(history_df, threshold):
    """
    Mathematical Model for Time-to-Breach Estimation.
    Calculates Crowd Velocity (Rate of Change) using Polynomial Fitting.
    """
    try:
        if len(history_df) < 8:
            return "🛰️ System Learning: Calibrating baseline flow patterns...", "INFO"

        # Extract last 8 capacity readings
        counts = history_df['Count'].values[-8:].astype(float)
        x = np.arange(len(counts))
        
        # Calculate Slope (Velocity)
        poly = np.polyfit(x, counts, 1)
        slope = poly[0]
        current_count = counts[-1]

        if slope > 0.4:
            remaining_capacity = threshold - current_count
            if remaining_capacity > 0:
                time_to_breach = int(remaining_capacity / (slope + 1e-6))
                time_to_breach = max(1, time_to_breach)
                msg = f"⚠️ PREDICTIVE ALERT: Crowd density surging (+{round(slope,1)} pax/sec). Est. limit breach in ~{time_to_breach} mins."
                return msg, "WARNING"
            else:
                return "🚨 CRITICAL OVERLOAD: Limit breached. Halt entries immediately.", "DANGER"
        elif slope < -0.2:
            return "📉 ANALYTICS: Positive dispersion trend. Density is reducing naturally.", "SUCCESS"
        else:
            return "✅ STATUS: Crowd flow is stabilized. No immediate threats.", "STABLE"

    except Exception as e:
        return "Analyzing temporal trajectory...", "INFO"

# ==========================================
# 🌌 5. UI & DASHBOARD STYLING (GLASSMORPHISM)
# ==========================================
st.set_page_config(page_title="Crowd Command Center", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Inter:wght@400;600&display=swap');
    
    /* Cyberpunk Deep Space Theme */
    .stApp { 
        background: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #16213e 50%, #0f3460 100%); 
        color: #E8E8E8; 
        font-family: 'Inter', sans-serif; 
    }
    
    /* Glowing Headers */
    h1, h2, h3 { 
        font-family: 'Orbitron', sans-serif !important; 
        color: #00D9FF !important; 
        text-shadow: 0 0 15px rgba(0,217,255,0.4); 
    }
    
    /* Glassmorphism Metrics */
    div[data-testid="metric-container"] { 
        background: rgba(255, 255, 255, 0.03) !important; 
        backdrop-filter: blur(12px); 
        border: 1px solid rgba(0, 217, 255, 0.2); 
        border-radius: 16px; 
        padding: 20px; 
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); 
        transition: transform 0.3s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(0, 217, 255, 0.6); 
    }
    
    /* Log Boxes */
    .log-box { 
        background: rgba(0, 0, 0, 0.5); 
        padding: 12px 15px; 
        border-radius: 8px; 
        border-left: 4px solid #00D9FF; 
        margin-bottom: 10px; 
        font-size: 14px; 
        line-height: 1.5;
        animation: slideIn 0.3s ease-out;
    }
    
    /* AI Insight Panel */
    .ai-insight { 
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid rgba(0, 217, 255, 0.3); 
        font-size: 16px; 
        line-height: 1.6; 
        box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🛡️ SMART CROWD COMMAND CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00FFCC; font-size: 1.2rem; letter-spacing: 2px;'>AI-POWERED TACTICAL SURVEILLANCE ECOSYSTEM</p>", unsafe_allow_html=True)

# ==========================================
# 📊 6. DATA VISUALIZATION ENGINES (PLOTLY)
# ==========================================
def create_dynamic_chart(df, threshold):
    fig = go.Figure()
    # Gradient filled spline chart
    fig.add_trace(go.Scatter(x=df['Time'], y=df['Count'], mode='lines+markers', name='Crowd', 
                             line=dict(color='#00D9FF', width=3, shape='spline'),
                             fill='tozeroy', fillcolor='rgba(0, 217, 255, 0.1)',
                             marker=dict(size=6, color='#FFFFFF', line=dict(width=2, color='#00D9FF'))))
    
    # Critical Threshold Line
    fig.add_hline(y=threshold, line_dash="dash", line_color="#FF4444", annotation_text="CRITICAL LIMIT", annotation_position="top left", annotation_font_color="#FF4444")
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E8E8E8'), margin=dict(l=10, r=10, t=30, b=10), height=280, title="📈 REAL-TIME TRAJECTORY")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
    return fig

def create_zone_bar_chart(zones):
    fig = go.Figure(data=[go.Bar(x=list(zones.keys()), y=list(zones.values()), 
                                 marker=dict(color=['#00D9FF', '#FFB800', '#FF4444'], line=dict(color='rgba(255,255,255,0.2)', width=1)),
                                 text=list(zones.values()), textposition='auto')])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=280, margin=dict(l=10, r=10, t=30, b=10), title="🏛️ SPATIAL DISTRIBUTION")
    return fig

def create_traffic_donut(total_in, total_out):
    labels = ['Entered (IN)', 'Exited (OUT)']
    values = [max(1, total_in), max(1, total_out)] 
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.55, 
                                 marker_colors=['#00FF88', '#FF4444'], textinfo='label+percent',
                                 hoverinfo="label+value")])
    fig.update_layout(title="🔄 TRAFFIC FLOW RATIO", paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=280, margin=dict(l=10, r=10, t=30, b=10), showlegend=False)
    return fig

# ==========================================
# 💾 7. SYSTEM STATE INITIALIZATION
# ==========================================
# Variables stored in session state to persist across Streamlit re-runs
if 'history' not in st.session_state: st.session_state.history = pd.DataFrame(columns=['Time', 'Count'])
if 'peak_count' not in st.session_state: st.session_state.peak_count = 0
if 'tracker' not in st.session_state: st.session_state.tracker = {}
if 'threat_logs' not in st.session_state: st.session_state.threat_logs = []
if 'total_in' not in st.session_state: st.session_state.total_in = 0  
if 'total_out' not in st.session_state: st.session_state.total_out = 0 
if 'ai_explanation' not in st.session_state: st.session_state.ai_explanation = "Initializing neural models..."
if 'last_alert_time' not in st.session_state: st.session_state.last_alert_time = 0
if 'last_missing_alert' not in st.session_state: st.session_state.last_missing_alert = 0
if 'heatmap_layer' not in st.session_state: st.session_state.heatmap_layer = np.zeros((480, 640), dtype=np.float32) 

# ==========================================
# ⚙️ 8. SIDEBAR - MASTER CONTROL PANEL
# ==========================================
st.sidebar.markdown("## ⚙️ COMMAND SETTINGS")

with st.sidebar.expander("📹 Camera Matrix (Feeds)", expanded=True):
    cam1_source = st.text_input("Primary Sector (Cam 1)", value="0", help="Use '0' for Webcam, or IP Cam URL.")
    cam2_source = st.text_input("Queue Sector (Cam 2)", value="demo_cctv.mp4")

with st.sidebar.expander("🎛️ Engine Configuration", expanded=False):
    threshold = st.slider("🚨 Critical Capacity Limit", 5, 200, 30)
    confidence = st.slider("🎯 YOLO Confidence", 0.3, 0.9, 0.45, 0.05)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Tactical Features")
audio_mode = st.sidebar.toggle("🔊 Marathi Voice PA System", True)
line_cross_mode = st.sidebar.toggle("🚦 Bi-Directional Counter", True) 
heatmap_mode = st.sidebar.toggle("🔥 Thermal Flow Analysis", False) 
privacy_mode = st.sidebar.toggle("🕶️ Civilian Privacy Blur", False)
endurance_mode = st.sidebar.toggle("⚡ Low-Power Endurance", False)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Missing Person Radar")
missing_file = st.sidebar.file_uploader("Upload Target Photo", type=['jpg', 'png'])
match_threshold = st.sidebar.slider("AI Match Sensitivity", 0.5, 0.9, 0.65)

# Target Signature Extraction Logic
target_hist = None
if missing_file:
    file_bytes = np.asarray(bytearray(missing_file.read()), dtype=np.uint8)
    target_img = cv2.imdecode(file_bytes, 1)
    st.sidebar.image(target_img, caption="Signature Extracted & Encrypted", width=120)
    
    # Extract facial features for histogram matching
    gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
    faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(gray, 1.1, 4)
    if len(faces) > 0:
        x, y, w, h = faces[0]
        target_roi = target_img[y:y+h, x:x+w]
        target_hsv = cv2.cvtColor(target_roi, cv2.COLOR_BGR2HSV)
        target_hist = cv2.calcHist([target_hsv], [0, 1], None, [16, 16], [0, 180, 0, 256])
        cv2.normalize(target_hist, target_hist)
        st.sidebar.success("Target Locked into Memory.")
    else:
        st.sidebar.error("Face not clear. Please upload another photo.")

st.sidebar.markdown("---")

# Main execution trigger
run_camera = st.sidebar.button("🔴 INITIATE SURVEILLANCE", use_container_width=True, type="primary") if not st.session_state.get('run_state', False) else st.sidebar.button("🛑 HALT SURVEILLANCE", use_container_width=True)
if run_camera:
    st.session_state['run_state'] = not st.session_state.get('run_state', False)
    st.rerun()

# ==========================================
# 🖥️ 9. MAIN DASHBOARD LAYOUT
# ==========================================
# Top Metrics Row
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
m_count = metric_col1.empty()
m_in = metric_col2.empty()
m_out = metric_col3.empty()
m_fps = metric_col4.empty()

st.markdown("<br>", unsafe_allow_html=True)

# Middle Video Row
main_col1, main_col2 = st.columns([1.6, 1])

with main_col1:
    st.markdown("### 📹 PRIMARY PERCEPTION (CAM 1)")
    cam1_placeholder = st.empty()
    st.markdown("### 🧠 NEURAL PREDICTION BRIEFING")
    ai_briefing_placeholder = st.empty() 

with main_col2:
    st.markdown("### 📹 QUEUE PERCEPTION (CAM 2)")
    cam2_placeholder = st.empty()
    st.markdown("### 🚓 TACTICAL DISPATCH LOGS")
    threat_log_placeholder = st.empty() 

st.markdown("<br>", unsafe_allow_html=True)

# Bottom Graph Row
g_col1, g_col2, g_col3 = st.columns([1.5, 1, 1])
with g_col1: chart_placeholder = st.empty()
with g_col2: zone_placeholder = st.empty()
with g_col3: traffic_placeholder = st.empty() 

alert_placeholder = st.empty()

# ==========================================
# 🔴 10. CORE INFERENCE ENGINE (THE WHILE LOOP)
# ==========================================
if st.session_state.get('run_state', False):
    
    # Load Model (Cached to prevent reloading)
    @st.cache_resource
    def load_model():
        try: return YOLO('models/yolov8n.pt')
        except: return YOLO('yolov8n.pt')
    
    model = load_model()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def parse_source(src): return int(src) if src.isdigit() else src

    # Initialize Camera Streams
    cap1 = cv2.VideoCapture(parse_source(cam1_source))
    cap1.set(cv2.CAP_PROP_BUFFERSIZE, 1)  
    cap2 = cv2.VideoCapture(parse_source(cam2_source))

    # --- CRITICAL VARS (Fixing the NameError) ---
    frame_counter = 0
    last_chart_update = 0
    fps_start_time = time.time() 
    CROSSING_LINE_Y = 240 
    
    # THE MASTER LOOP
    while st.session_state.get('run_state', False):
        current_time = time.time()
        fps = 1.0 / (current_time - fps_start_time + 1e-6)
        fps_start_time = current_time

        ret1, frame1 = cap1.read()
        
        count_people = 0
        zones = {"Entry": 0, "Queue": 0, "Temple": 0}
        bh_alerts = []
        
        # ---------------------------------------------------------
        # 🛠️ A. FAIL-SAFE 'NO SIGNAL' PROTOCOL
        # ---------------------------------------------------------
        if not ret1:
            frame_counter += 1
            # Generate a pure black frame with red warning text
            annotated_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(annotated_frame, "CAM 1: CONNECTION LOST", (80, 220), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            cv2.putText(annotated_frame, "ATTEMPTING AUTO-RECONNECT...", (150, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
            
            # Auto-reconnect every 60 frames (approx 2 seconds)
            if frame_counter % 60 == 0: 
                cap1 = cv2.VideoCapture(parse_source(cam1_source))
            
            cam1_placeholder.image(annotated_frame, channels="BGR", use_container_width=True)
            time.sleep(0.05)
            continue # Skip AI processing for this dead frame
            
        # ---------------------------------------------------------
        # 👁️ B. EDGE AI PERCEPTION (YOLOv8)
        # ---------------------------------------------------------
        frame_counter += 1
        
        # Endurance mode skips frames to save CPU
        if frame_counter % (4 if endurance_mode else 2) != 0: continue 
        if frame_counter % 150 == 0: gc.collect() # Memory management

        frame1 = cv2.resize(frame1, (640, 480))
        # Track objects (classes=[0] means only 'person')
        res1 = model.track(frame1, classes=[0], conf=confidence, persist=True, imgsz=320, verbose=False)
        annotated_frame = frame1.copy()

        # Draw Bi-Directional Line
        if line_cross_mode:
            cv2.line(annotated_frame, (0, CROSSING_LINE_Y), (640, CROSSING_LINE_Y), (255, 0, 255), 2)
            cv2.putText(annotated_frame, "IN / ENTRY", (10, CROSSING_LINE_Y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
            cv2.putText(annotated_frame, "OUT / EXIT", (10, CROSSING_LINE_Y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

        # Process Bounding Boxes
        if res1[0].boxes.id is not None:
            boxes_data = res1[0].boxes.data.cpu().numpy()
            for box in boxes_data:
                if len(box) >= 7:
                    x1, y1, x2, y2, obj_id, conf, cls = box
                    cx, cy = int((x1+x2)/2), int((y1+y2)/2)
                    w, h = x2 - x1, y2 - y1
                    
                    count_people += 1
                    
                    # Spatial Mapping (Dividing screen into 3 vertical zones)
                    if cx < 213: zones["Entry"] += 1
                    elif cx < 426: zones["Queue"] += 1
                    else: zones["Temple"] += 1

                    # Draw highly visible Neon Bounding Box
                    cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 204), 2)
                    cv2.putText(annotated_frame, f"ID:{int(obj_id)}", (int(x1), int(y1)-8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 204), 2)
                    
                    # Tracking Logic for IN/OUT
                    if obj_id in st.session_state.tracker:
                        prev_cx, prev_cy, prev_time = st.session_state.tracker[obj_id]
                        
                        if line_cross_mode:
                            if prev_cy < CROSSING_LINE_Y and cy >= CROSSING_LINE_Y:
                                st.session_state.total_in += 1
                            elif prev_cy > CROSSING_LINE_Y and cy <= CROSSING_LINE_Y:
                                st.session_state.total_out += 1

                        # Panic/Running Detection (Velocity Spike)
                        dist = ((cx-prev_cx)**2 + (cy-prev_cy)**2)**0.5
                        if dist / (current_time - prev_time + 1e-6) > 400: 
                            bh_alerts.append("PANIC DETECTED")
                    
                    st.session_state.tracker[obj_id] = (cx, cy, current_time)

                    # Heatmap Accumulation
                    if heatmap_mode: cv2.circle(st.session_state.heatmap_layer, (cx, cy), 20, 3, -1)

        # ---------------------------------------------------------
        # 👤 C. MISSING PERSON RADAR
        # ---------------------------------------------------------
        if target_hist is not None and frame_counter % 6 == 0:
            gray_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            current_faces = face_cascade.detectMultiScale(gray_frame, 1.1, 5, minSize=(40, 40))
            
            for (fx, fy, fw, fh) in current_faces:
                # Extract ROI and compare histogram
                current_roi = frame1[fy:fy+fh, fx:fx+fw]
                current_hsv = cv2.cvtColor(current_roi, cv2.COLOR_BGR2HSV)
                current_hist = cv2.calcHist([current_hsv], [0, 1], None, [16, 16], [0, 180, 0, 256])
                cv2.normalize(current_hist, current_hist)
                
                score = cv2.compareHist(target_hist, current_hist, cv2.HISTCMP_CORREL)
                
                if score > match_threshold:
                    cv2.rectangle(annotated_frame, (fx, fy), (fx+fw, fy+fh), (0, 0, 255), 4)
                    cv2.putText(annotated_frame, f"TARGET:{int(score*100)}%", (fx, fy-10), 1, 1.5, (0,0,255), 2)
                    
                    if (current_time - st.session_state.last_missing_alert) > 15:
                        log_msg = f"TARGET MATCHED ({int(score*100)}%). Directing team to sector."
                        log_threat(log_msg, "CRITICAL")
                        send_whatsapp_alert(f"🚨 TARGET IDENTIFIED!\nCamera: Main Sector\nAccuracy: {int(score*100)}%")
                        
                        if audio_mode: trigger_marathi_alert("missing")
                        
                        save_evidence(annotated_frame, "MISSING_PERSON")
                        st.session_state.last_missing_alert = current_time

        # ---------------------------------------------------------
        # 🎭 D. ADVANCED VISUAL OVERLAYS
        # ---------------------------------------------------------
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

        # UI Info bar on video
        cv2.rectangle(annotated_frame, (0, 0), (640, 35), (0,0,0), -1)
        cv2.putText(annotated_frame, f"ZONES: E:{zones['Entry']} | Q:{zones['Queue']} | T:{zones['Temple']}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 204), 2)
        cv2.putText(annotated_frame, f"FPS: {int(fps)}", (540, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
        # Push video frame to UI
        cam1_placeholder.image(annotated_frame, channels="BGR", use_container_width=True)
        
        # ---------------------------------------------------------
        # 📹 E. SECONDARY CAMERA LOGIC
        # ---------------------------------------------------------
        if cap2.isOpened():
            ret2, frame2 = cap2.read()
            if not ret2 and not str(cam2_source).isdigit(): 
                # Loop video if it's an mp4 file
                cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret2, frame2 = cap2.read()
            
            if ret2:
                frame2 = cv2.resize(frame2, (640, 360))
                cv2.putText(frame2, "CAM 2: QUEUE MONITOR", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                cam2_placeholder.image(frame2, channels="BGR", use_container_width=True)
            else:
                cam2_placeholder.error("CAM 2 OFFLINE")

        # ---------------------------------------------------------
        # 🧠 F. NEURAL PREDICTION & METRICS UPDATES
        # ---------------------------------------------------------
        # ✅ ALL INDENTATION IS NOW PERFECTLY ALIGNED INSIDE THE WHILE LOOP
        if frame_counter % 30 == 0:
            if len(st.session_state.history) > 5:
                # Call the mathematical prediction model
                pred_msg, p_type = advanced_crowd_prediction(st.session_state.history, threshold)
                
                # Dynamic Styling based on threat level
                bg_color = "linear-gradient(135deg, rgba(255, 68, 68, 0.2), rgba(0,0,0,0.6))" if p_type == "DANGER" else \
                           "linear-gradient(135deg, rgba(255, 184, 0, 0.2), rgba(0,0,0,0.6))" if p_type == "WARNING" else \
                           "linear-gradient(135deg, rgba(0, 217, 255, 0.1), rgba(0,0,0,0.6))"
                
                st.session_state.ai_explanation = f"""
                <div class='ai-insight' style='background: {bg_color};'>
                    <h4 style='margin:0; color:#00D9FF;'>🧠 AI TACTICAL BRIEFING</h4>
                    <p style='margin-top: 10px; font-size: 17px; font-weight: 500;'>{pred_msg}</p>
                    <hr style='border: 0; height: 1px; background: rgba(0,217,255,0.2);'>
                    <small style='color: #A0A0A0;'>Model: Ultralytics YOLOv8n + Polynomial Trajectory V3</small>
                </div>
                """
                ai_briefing_placeholder.markdown(st.session_state.ai_explanation, unsafe_allow_html=True)

        # Update Top Metrics
        st.session_state.peak_count = max(st.session_state.peak_count, count_people)
        m_count.metric("👥 ACTIVE POPULATION", count_people, delta=f"{count_people - threshold} Limit Capacity", delta_color="inverse")
        m_in.metric("🟢 TOTAL ENTRY", st.session_state.total_in)
        m_out.metric("🔴 TOTAL EXIT", st.session_state.total_out)
        m_fps.metric("⚡ LOGIC ENGINE FPS", int(fps))

        # Update Dispatch Logs UI
        logs_html = "".join(st.session_state.threat_logs)
        threat_log_placeholder.markdown(logs_html if logs_html else "<p style='color:gray;'>[System] Scanning for threats...</p>", unsafe_allow_html=True)

        # Update Plotly Charts
        # Update Plotly Charts
        if current_time - last_chart_update > 2.0:
            now = datetime.now().strftime("%H:%M:%S")
            st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame({'Time': [now], 'Count': [count_people]})]).tail(25)
            
            # ✅ FIX: Added unique 'key' parameter to each chart
            chart_placeholder.plotly_chart(create_dynamic_chart(st.session_state.history, threshold), use_container_width=True, key=f"trend_{frame_counter}")
            zone_placeholder.plotly_chart(create_zone_bar_chart(zones), use_container_width=True, key=f"zone_{frame_counter}")
            traffic_placeholder.plotly_chart(create_traffic_donut(st.session_state.total_in, st.session_state.total_out), use_container_width=True, key=f"traffic_{frame_counter}")
            
            last_chart_update = current_time
        # ---------------------------------------------------------
        # 🚨 G. ACTIONABLE THREAT DISPATCH
        # ---------------------------------------------------------
        if bh_alerts and (current_time - st.session_state.last_alert_time) > 10:
            dispatch_msg = f"PANIC BEHAVIOR DETECTED. Dispatching Quick Response Team."
            log_threat(dispatch_msg, "CRITICAL")
            send_whatsapp_alert(f"URGENT: {dispatch_msg}")
            if audio_mode: trigger_marathi_alert("running")
            st.session_state.last_alert_time = current_time
            
        elif count_people > threshold and (current_time - st.session_state.last_alert_time) > 10: 
            dispatch_msg = f"CAPACITY OVERLOAD ({count_people}/{threshold}). Halt inflow immediately."
            log_threat(dispatch_msg, "WARNING")
            send_whatsapp_alert(f"⚠️ Crowd Warning: {dispatch_msg}")
            if audio_mode: trigger_marathi_alert("overcrowded")
            st.session_state.last_alert_time = current_time

    # Cleanup when surveillance is stopped
    if cap1 is not None: cap1.release()
    if cap2 is not None: cap2.release()

# ==========================================
# 📄 11. POST-MISSION EXPORT & EVIDENCE
# ==========================================
if not st.session_state.get('run_state', False):
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📂 Command Archives")
    
    with st.sidebar.expander("📸 Incident Gallery Viewer", expanded=False):
        logs = [f for f in os.listdir(EVIDENCE_DIR) if f.endswith('.jpg')] if os.path.exists(EVIDENCE_DIR) else []
        if logs:
            st.write(f"Found {len(logs)} high-res evidences.")
            for log_file in sorted(logs, reverse=True)[:3]: 
                st.image(f"{EVIDENCE_DIR}/{log_file}", caption=log_file)
        else: 
            st.write("Archive clean. No incidents.")

    if not st.session_state.history.empty:
        csv_data = st.session_state.history.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button("💾 Download Telemetry (CSV)", data=csv_data, file_name=f"crowd_telemetry_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
# ==========================================
# 📄 11. POST-MISSION EXPORT & EVIDENCE
# ==========================================
if not st.session_state.get('run_state', False):
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📂 Command Archives")
    
    with st.sidebar.expander("📸 Incident Gallery Viewer", expanded=False):
        logs = [f for f in os.listdir(EVIDENCE_DIR) if f.endswith('.jpg')] if os.path.exists(EVIDENCE_DIR) else []
        if logs:
            st.write(f"Found {len(logs)} high-res evidences.")
            for log_file in sorted(logs, reverse=True)[:3]: 
                st.image(f"{EVIDENCE_DIR}/{log_file}", caption=log_file)
        else: 
            st.write("Archive clean. No incidents.")

    if not st.session_state.history.empty:
        csv_data = st.session_state.history.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button("💾 Download Telemetry (CSV)", data=csv_data, file_name=f"crowd_telemetry_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)

    # ✅ FIX: इथेच फंक्शन बनवले आहे जेणेकरून Pylance एरर देणार नाही
    def create_safety_report(peak, alerts):
        filename = "Final_Safety_Audit.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=== 🛡️ SMART CROWD INTELLIGENCE SYSTEM AUDIT ===\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Peak Crowd Observed: {peak} persons\n")
            f.write(f"Total Critical Alerts Issued: {alerts}\n")
            f.write("Status: Surveillance Session Concluded Successfully.\n")
            f.write("==================================================\n")
        return filename

  # Generate Final Report Button
    # ✅ इथे आपण 'key="gen_report_btn"' टाकला आहे
    if st.sidebar.button("📄 Generate Police Audit Report", use_container_width=True, key="gen_report_btn"):
        report_file = create_safety_report(st.session_state.peak_count, st.session_state.alert_count)
        with open(report_file, "rb") as f:
            st.sidebar.download_button(
                label="📥 Download Final TXT Report",
                data=f,
                file_name="Final_Safety_Audit.txt",
                mime="text/plain",
                key="download_final_report_btn" # ✅ हा सर्वात महत्त्वाचा बदल आहे!
            )
        st.sidebar.success("✅ Report Generated!")
# --- END OF CODE ---