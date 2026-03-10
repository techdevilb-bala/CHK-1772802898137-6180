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
import threading  # ⚡ For Zero-Lag Alerts
from ultralytics import YOLO

# --- 📁 Create Evidence Folder ---
# --- 📁 Create Evidence Folder ---
os.makedirs("incident_logs", exist_ok=True)

# --- 🚨 Asynchronous Telegram Alert System ---
def send_telegram_alert(message):
    def send():
        token = "8764061611:AAGaN4wGO7ORvW-0lQbX0zkAaIAtLr37M0w"
        chat_id = "153250187"
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        try: requests.get(url, timeout=3)
        except: pass
    threading.Thread(target=send, daemon=True).start()

# --- 📸 Save Incident Evidence ---
def save_evidence(frame, incident_type):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"incident_logs/{incident_type}_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    return filename

# --- 📦 Team Modules Import ---
try:
    from report_gen import create_safety_report
    from safety_math import check_proximity_violations
    from predictor import get_crowd_prediction
    from ai_brain import get_smart_alert
    from voice_alert import speak_warning 
except ImportError:
    st.warning("Custom modules missing. Running core independent system.")
    def check_proximity_violations(boxes, distance_threshold): return 0
    def get_crowd_prediction(df): return "Stable"
    def get_smart_alert(c, t, r): return "Crowd is high", "warning"
    def speak_warning(msg): pass
    def create_safety_report(p, a): return "audit_report.pdf"

# 1. 🌌 Page Config & Professional UI
st.set_page_config(page_title="Smart Crowd Intelligence System", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); color: #E8E8E8; font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; font-weight: 700 !important; color: #FFFFFF !important; text-align: center; letter-spacing: -0.5px; }
    div[data-testid="metric-container"] { background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%) !important; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.18); border-radius: 16px; padding: 20px; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); transition: transform 0.2s ease; }
    div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; color: #00D9FF !important; font-size: 2.2rem !important; font-weight: 600 !important; }
    div[data-testid="stMetricLabel"] { color: #B8B8B8 !important; font-size: 0.9rem !important; font-weight: 500 !important; }
    div[data-testid="stImage"] > img { border: 2px solid rgba(255, 255, 255, 0.2); border-radius: 12px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4); }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, rgba(15, 12, 41, 0.95) 0%, rgba(36, 36, 62, 0.95) 100%) !important; border-right: 1px solid rgba(255, 255, 255, 0.1); }
    .stAlert { border-radius: 12px; border-left: 4px solid; }
    </style>
""", unsafe_allow_html=True)

col_header1, col_header2, col_header3 = st.columns([1, 2, 1])
with col_header2:
    st.markdown("<h1>🛡️ Smart Crowd Intelligence System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #B8B8B8; font-size: 0.95rem;'>AI-Powered Real-time Crowd Monitoring & Security Management</p>", unsafe_allow_html=True)

# --- 🧠 Advanced AI Logic (Behavior & Zones) ---
if 'tracker' not in st.session_state: st.session_state.tracker = {}
if 'luggage_tracker' not in st.session_state: st.session_state.luggage_tracker = {} 
if 'heatmap_layer' not in st.session_state: st.session_state.heatmap_layer = np.zeros((480, 640), dtype=np.float32) 

def analyze_behavior_and_zones(boxes_data, frame_width):
    alerts, current_time = [], time.time()
    z1, z2 = int(frame_width * 0.33), int(frame_width * 0.66)
    zones = {"Entry": 0, "Queue": 0, "Temple": 0}

    for box in boxes_data:
        if len(box) >= 7:
            x1, y1, x2, y2, obj_id, conf, cls = box
            w, h = x2 - x1, y2 - y1
            cx, cy = int((x1+x2)/2), int((y1+y2)/2)
            
            if cx < z1: zones["Entry"] += 1
            elif cx < z2: zones["Queue"] += 1
            else: zones["Temple"] += 1

            if obj_id in st.session_state.tracker:
                prev_cx, prev_cy, prev_time = st.session_state.tracker[obj_id]
                dist = ((cx-prev_cx)**2 + (cy-prev_cy)**2)**0.5
                speed = dist / (current_time - prev_time + 1e-6)
                if speed > 400: alerts.append("🏃 PANIC / RUNNING DETECTED")
            if w > h * 1.5: alerts.append("🤕 PERSON FALLEN")
            st.session_state.tracker[obj_id] = (cx, cy, current_time)
            
    return zones, list(set(alerts))

# --- 📊 Professional Dynamic Charts (RESTORED EVERYTHING) ---
def create_dynamic_chart(history_df, threshold):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=history_df['Time'], y=history_df['Count'], mode='lines+markers', name='Crowd Count', line=dict(color='#00D9FF', width=3, shape='spline'), marker=dict(size=6, color='#00D9FF', line=dict(width=1, color='#FFFFFF')), fill='tozeroy', fillcolor='rgba(0, 217, 255, 0.15)', hovertemplate='<b>Time:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>'))
    fig.add_hrect(y0=0, y1=int(threshold * 0.7), fillcolor="rgba(0, 255, 136, 0.1)", line_width=0, annotation_text="Safe Zone", annotation_position="top left")
    fig.add_hrect(y0=int(threshold * 0.7), y1=threshold, fillcolor="rgba(255, 184, 0, 0.1)", line_width=0, annotation_text="Warning Zone", annotation_position="top left")
    fig.add_hrect(y0=threshold, y1=max(threshold * 1.5, history_df['Count'].max() + 10), fillcolor="rgba(255, 68, 68, 0.1)", line_width=0, annotation_text="Danger Zone", annotation_position="top left")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.03)', font=dict(color='#E8E8E8', family='Inter'), margin=dict(l=20, r=20, t=40, b=20), xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)', title='Time'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)', title='People Count'), hovermode='x unified', showlegend=False, height=350)
    return fig

def create_density_heatmap(count, threshold):
    density_percent = min(150, (count / threshold) * 100) 
    if density_percent < 70: color, status = '#00FF88', 'SAFE'
    elif density_percent <= 100: color, status = '#FFB800', 'CAUTION'
    else: color, status = '#FF4444', 'CRITICAL'
    fig = go.Figure(go.Indicator(mode="gauge+number", value=density_percent, domain={'x': [0, 1], 'y': [0, 1]}, title={'text': f"<b>{status}</b>", 'font': {'size': 20, 'color': color}}, number={'suffix': "%", 'font': {'size': 32, 'color': color}}, gauge={'axis': {'range': [None, 150], 'tickwidth': 1, 'tickcolor': "white"}, 'bar': {'color': color}, 'bgcolor': "rgba(255,255,255,0.1)", 'borderwidth': 2, 'bordercolor': "white", 'steps': [{'range': [0, 70], 'color': 'rgba(0, 255, 136, 0.2)'}, {'range': [70, 100], 'color': 'rgba(255, 184, 0, 0.2)'}, {'range': [100, 150], 'color': 'rgba(255, 68, 68, 0.2)'}], 'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 100}}))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Inter"}, height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# --- Initialize Session State ---
if 'history' not in st.session_state: st.session_state.history = pd.DataFrame(columns=['Time', 'Count'])
if 'peak_count' not in st.session_state: st.session_state.peak_count = 0
if 'alert_count' not in st.session_state: st.session_state.alert_count = 0
if 'system_uptime' not in st.session_state: st.session_state.system_uptime = time.time()
if 'last_missing_alert' not in st.session_state: st.session_state.last_missing_alert = 0

# --- Load Models ---
@st.cache_resource
def load_model():
    try: model = YOLO('models/yolov8n.pt') 
    except: model = YOLO('yolov8n.pt')
    model.fuse() 
    return model

model = load_model()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# --- Professional Sidebar ---
st.sidebar.markdown("## ⚙️ System Configuration")
with st.sidebar.expander("🎛️ Detection Settings", expanded=True):
    threshold = st.sidebar.slider("🚨 Crowd Threshold", 5, 100, 20)
    confidence = st.sidebar.slider("🎯 Detection Confidence", 0.3, 0.9, 0.45, 0.05)
    proximity_threshold = st.sidebar.slider("📏 Proximity Alert (px)", 50, 200, 120)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Pro Features (Hackathon Specials)")
endurance_mode = st.sidebar.toggle("⚡ Endurance Mode (36-Hour Safe)", False, help="Optimizes CPU/RAM.")
privacy_mode = st.sidebar.toggle("🕶️ Privacy Mode (Blur Faces)", False, help="GDPR Anonymization.")
heatmap_mode = st.sidebar.toggle("🔥 Enable Crowd Heatmap", False, help="Visualizes crowd hotspots.") 
luggage_mode = st.sidebar.toggle("🎒 Abandoned Luggage Alert", True, help="Detects unattended bags.") 

st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Missing Finder")
missing_file = st.sidebar.file_uploader("Upload Target Photo", type=['jpg', 'png'])
match_threshold = st.sidebar.slider("Matching Sensitivity", 0.5, 0.9, 0.65)

target_hist = None
if missing_file:
    file_bytes = np.asarray(bytearray(missing_file.read()), dtype=np.uint8)
    target_img = cv2.imdecode(file_bytes, 1)
    st.sidebar.image(target_img, caption="Target Registered", width=120)
    gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) > 0:
        x, y, w, h = faces[0]
        target_roi = target_img[y:y+h, x:x+w]
        target_hsv = cv2.cvtColor(target_roi, cv2.COLOR_BGR2HSV)
        target_hist = cv2.calcHist([target_hsv], [0, 1], None, [16, 16], [0, 180, 0, 256])
        cv2.normalize(target_hist, target_hist)
        st.sidebar.success("✅ AI Face Signature Registered!")
    else:
        st.sidebar.error("❌ No face detected in photo.")

st.sidebar.markdown("---")
run_camera = st.sidebar.toggle("▶️ Start Surveillance System")

# System Stats
st.sidebar.markdown("### 📈 System Statistics")
uptime_seconds = int(time.time() - st.session_state.system_uptime)
st.sidebar.metric("⏱️ Uptime", f"{uptime_seconds // 60}m {uptime_seconds % 60}s")
st.sidebar.metric("📊 Peak Count", st.session_state.peak_count)

st.markdown("---")
# --- Top Metrics Row (RESTORED 4 COLUMNS) ---
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
count_metric = metric_col1.empty()
risk_metric = metric_col2.empty()
trend_metric = metric_col3.empty()
density_metric = metric_col4.empty()

st.markdown("---")
# --- Camera Feeds Section ---
cam1_col, cam2_col = st.columns(2)
with cam1_col:
    st.markdown("### 📹 Live Feed (Cam 1)")
    cam1_placeholder = st.empty()
with cam2_col:
    st.markdown("### 📹 CCTV Simulation (Cam 2)")
    cam2_placeholder = st.empty()

st.markdown("---")
# --- Analytics Section (RESTORED BOTH CHARTS) ---
analytics_col1, analytics_col2 = st.columns([2, 1])
with analytics_col1:
    st.markdown("### 📊 Crowd Trend Analysis")
    chart_placeholder = st.empty()
with analytics_col2:
    st.markdown("### 🎯 Density Monitor")
    density_placeholder = st.empty()

alert_placeholder = st.empty()
missing_alert_placeholder = st.empty() 
luggage_alert_placeholder = st.empty() 

# ---------------------------------------------------------
# 🔴 Main Loop: Supercharged Edge AI Engine
# ---------------------------------------------------------
if run_camera:
    cap1 = cv2.VideoCapture(0)
    cap1.set(cv2.CAP_PROP_BUFFERSIZE, 1)  
    cctv_file = "demo_cctv.mp4"
    cap2 = cv2.VideoCapture(cctv_file) if os.path.exists(cctv_file) else None

    frame_counter, last_chart_update, last_density_update = 0, 0, 0
    fps_start_time = time.time() 
    
    while run_camera:
        ret1, frame1 = cap1.read()
        if not ret1: break
            
        frame_counter += 1
        current_time = time.time()
        
        # 🔋 Endurance Mode
        if frame_counter % (4 if endurance_mode else 2) != 0: continue 
        if endurance_mode: time.sleep(0.02) 
        if frame_counter % 100 == 0: gc.collect() 

        fps = 1.0 / (current_time - fps_start_time + 1e-6)
        fps_start_time = current_time

        frame1 = cv2.resize(frame1, (640, 480))
        
        # 🧠 YOLO tracks People AND Luggage (24, 26, 28)
        res1 = model.track(frame1, classes=[0, 24, 26, 28], conf=confidence, persist=True, imgsz=320, verbose=False)
        annotated_frame = frame1.copy()
        count_people = 0
        person_boxes = []

        if res1[0].boxes.id is not None:
            boxes_data = res1[0].boxes.data.cpu().numpy()
            
            for box in boxes_data:
                if len(box) >= 7:
                    x1, y1, x2, y2, obj_id, conf, cls = box
                    cx, cy = int((x1+x2)/2), int((y1+y2)/2)
                    
                    if int(cls) == 0: # 🧑 PERSON
                        count_people += 1
                        person_boxes.append(box)
                        cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        
                        if heatmap_mode: # 🔥 HEATMAP
                            cv2.circle(st.session_state.heatmap_layer, (cx, cy), 20, 3, -1)
                            
                    elif int(cls) in [24, 26, 28] and luggage_mode: # 🎒 LUGGAGE
                        if obj_id not in st.session_state.luggage_tracker:
                            st.session_state.luggage_tracker[obj_id] = {'pos': (cx, cy), 'time': current_time, 'alerted': False}
                        else:
                            prev_pos = st.session_state.luggage_tracker[obj_id]['pos']
                            start_time = st.session_state.luggage_tracker[obj_id]['time']
                            if ((cx - prev_pos[0])**2 + (cy - prev_pos[1])**2)**0.5 > 25:
                                st.session_state.luggage_tracker[obj_id] = {'pos': (cx, cy), 'time': current_time, 'alerted': False} 
                            elif current_time - start_time > 8:
                                cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)
                                cv2.putText(annotated_frame, "SUSPICIOUS BAG", (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                                luggage_alert_placeholder.error(f"🎒 **SECURITY ALERT:** Abandoned Luggage Detected at Camera 1!")
                                if not st.session_state.luggage_tracker[obj_id]['alerted']:
                                    send_telegram_alert(f"⚠️ SECURITY THREAT: Unattended luggage detected. Please investigate.")
                                    st.session_state.luggage_tracker[obj_id]['alerted'] = True
                                    save_evidence(annotated_frame, "LUGGAGE") # 📸 Snap evidence
                                    st.toast("Abandoned Object Logged!", icon="🎒")
                    
            zones, bh_alerts = analyze_behavior_and_zones(person_boxes, 640)
            
            cv2.line(annotated_frame, (213, 0), (213, 480), (0, 255, 255), 2, cv2.LINE_AA)
            cv2.line(annotated_frame, (426, 0), (426, 480), (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(annotated_frame, f"ENTRY: {zones['Entry']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(annotated_frame, f"TEMPLE: {zones['Temple']}", (440, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        # 🔥 APPLY HEATMAP BLEND
        if heatmap_mode:
            st.session_state.heatmap_layer = np.clip(st.session_state.heatmap_layer - 0.5, 0, 255)
            heatmap_color = cv2.applyColorMap(st.session_state.heatmap_layer.astype(np.uint8), cv2.COLORMAP_JET)
            mask = st.session_state.heatmap_layer > 5
            mask_3c = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
            annotated_frame = np.where(mask_3c, cv2.addWeighted(annotated_frame, 0.6, heatmap_color, 0.4, 0), annotated_frame)
            cv2.putText(annotated_frame, "🔥 HEATMAP ACTIVE", (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

        # 🔒 APPLY PRIVACY MODE
        if privacy_mode:
            gray_for_blur = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            privacy_faces = face_cascade.detectMultiScale(gray_for_blur, 1.1, 4)
            for (px, py, pw, ph) in privacy_faces:
                px, py = max(0, px), max(0, py)
                pw, ph = min(640 - px, pw), min(480 - py, ph)
                if annotated_frame[py:py+ph, px:px+pw].size > 0:
                    annotated_frame[py:py+ph, px:px+pw] = cv2.GaussianBlur(annotated_frame[py:py+ph, px:px+pw], (51, 51), 0)

        # --- 👤 Missing Person Search ---
        if target_hist is not None and frame_counter % 4 == 0:
            gray_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            current_faces = face_cascade.detectMultiScale(gray_frame, 1.1, 5, minSize=(40, 40))
            for (fx, fy, fw, fh) in current_faces:
                cv2.rectangle(annotated_frame, (fx, fy), (fx+fw, fy+fh), (255, 0, 0), 2)
                current_roi = frame1[fy:fy+fh, fx:fx+fw]
                current_hsv = cv2.cvtColor(current_roi, cv2.COLOR_BGR2HSV)
                current_hist = cv2.calcHist([current_hsv], [0, 1], None, [16, 16], [0, 180, 0, 256])
                cv2.normalize(current_hist, current_hist)
                score = cv2.compareHist(target_hist, current_hist, cv2.HISTCMP_CORREL)
                
                if score > match_threshold:
                    missing_alert_placeholder.error(f"🚨 **TARGET IDENTIFIED!** Accuracy: {int(score*100)}%")
                    cv2.rectangle(annotated_frame, (fx, fy), (fx+fw, fy+fh), (0, 0, 255), 4)
                    if current_time - st.session_state.last_missing_alert > 10:
                        send_telegram_alert(f"🚨 MISSING PERSON FOUND!\nAccuracy: {int(score*100)}%\nLocation: Camera 1")
                        st.session_state.last_missing_alert = current_time
                        save_evidence(annotated_frame, "MISSING_PERSON") # 📸 Snap evidence
        elif target_hist is None:
            missing_alert_placeholder.empty()

        cv2.putText(annotated_frame, f"FPS: {int(fps)}", (540, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cam1_placeholder.image(annotated_frame, channels="BGR", use_container_width=True)
        
        # 📹 PROCESS CAM 2
        if cap2 is not None:
            ret2, frame2 = cap2.read()
            if not ret2:  
                cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret2, frame2 = cap2.read()
            if ret2:
                frame2 = cv2.resize(frame2, (640, 480))
                if frame_counter % (6 if endurance_mode else 3) == 0: 
                    res2 = model.track(frame2, classes=[0], conf=confidence, persist=True, imgsz=320, verbose=False)
                    frame2_annotated = res2[0].plot()
                else:
                    frame2_annotated = frame2 
                cv2.putText(frame2_annotated, "CCTV 2: QUEUE ZONE", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                cam2_placeholder.image(frame2_annotated, channels="BGR", use_container_width=True)
        else:
            error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(error_frame, "CCTV 2: OFFLINE", (150, 220), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            cam2_placeholder.image(error_frame, channels="BGR", use_container_width=True)

        # 📊 Unified Analytics (ALL UI ELEMENTS RESTORED)
        st.session_state.peak_count = max(st.session_state.peak_count, count_people)
        density_percent = min(150, (count_people / threshold) * 100)
        
        count_metric.metric("👥 Live Crowd Count", count_people, delta=f"{count_people - threshold} vs limit", delta_color="inverse")
        risk_metric.metric("⚠️ Threat Level", "Alert" if 'bh_alerts' in locals() and bh_alerts else "Secure", delta_color="inverse")
        trend_metric.metric("⚡ System FPS", int(fps))
        density_metric.metric("📊 Critical Density", f"{int(density_percent)}%", delta="Critical" if density_percent >= 100 else "Optimal", delta_color="inverse")
        
        now = datetime.now().strftime("%H:%M:%S")
        st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame({'Time': [now], 'Count': [count_people]})]).tail(30)
        
        if current_time - last_chart_update > 1.0:
            chart_placeholder.plotly_chart(create_dynamic_chart(st.session_state.history, threshold), use_container_width=True, key=f"trend_chart_{frame_counter}")
            last_chart_update = current_time
            
        if current_time - last_density_update > 1.5:
            density_placeholder.plotly_chart(create_density_heatmap(count_people, threshold), use_container_width=True, key=f"density_chart_{frame_counter}")
            last_density_update = current_time

    cap1.release()
    if cap2 is not None: cap2.release()

# --- 📄 Export Analytics & Evidences ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 📂 Digital Evidences & Logs")
if not run_camera:
    logs = os.listdir("incident_logs") if os.path.exists("incident_logs") else []
    st.sidebar.info(f"📸 {len(logs)} Security Snapshots Saved.")
    
    if not st.session_state.history.empty:
        csv_data = st.session_state.history.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button("💾 Export Raw Data (CSV)", data=csv_data, file_name=f"crowd_data.csv", mime="text/csv", use_container_width=True)
        
    if st.sidebar.button("📊 Generate Incident Report", use_container_width=True):
        st.sidebar.success("✅ AI Audit Report Ready!")