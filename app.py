import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import streamlit as st
import cv2
from ultralytics import YOLO
import time
import os
import requests
import numpy as np

# --- Team Modules Import ---
from report_gen import create_safety_report
from safety_math import check_proximity_violations
from predictor import get_crowd_prediction
from ai_brain import get_smart_alert
from voice_alert import speak_warning 

# 1. 🌌 Page Config & Professional UI
st.set_page_config(
    page_title="Smart Crowd Intelligence System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS with Performance Optimization
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #E8E8E8;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        text-align: center;
        letter-spacing: -0.5px;
    }
    
    /* Metric Cards - Professional Design */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: transform 0.2s ease;
    }
    
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: #00D9FF !important;
        font-size: 2.2rem !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #B8B8B8 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    /* Camera Feed Styling */
    div[data-testid="stImage"] > img {
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    
    /* Sidebar Professional Look */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 12, 41, 0.95) 0%, rgba(36, 36, 62, 0.95) 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Alert Boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
    }
    </style>
""", unsafe_allow_html=True)

# Header with System Status
col_header1, col_header2, col_header3 = st.columns([1, 2, 1])
with col_header2:
    st.markdown("<h1>🛡️ Smart Crowd Intelligence System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #B8B8B8; font-size: 0.95rem;'>AI-Powered Real-time Crowd Monitoring & Safety Management</p>", unsafe_allow_html=True)

# --- 📊 Professional Dynamic Chart ---
def create_dynamic_chart(history_df, threshold):
    fig = go.Figure()
    
    # Main trend line with gradient fill
    fig.add_trace(go.Scatter(
        x=history_df['Time'], 
        y=history_df['Count'],
        mode='lines+markers',
        name='Crowd Count',
        line=dict(color='#00D9FF', width=3, shape='spline'),
        marker=dict(size=6, color='#00D9FF', line=dict(width=1, color='#FFFFFF')),
        fill='tozeroy',
        fillcolor='rgba(0, 217, 255, 0.15)',
        hovertemplate='<b>Time:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>'
    ))
    
    # Threshold zones
    fig.add_hrect(y0=0, y1=int(threshold * 0.7), fillcolor="rgba(0, 255, 136, 0.1)", line_width=0, annotation_text="Safe Zone", annotation_position="top left")
    fig.add_hrect(y0=int(threshold * 0.7), y1=threshold, fillcolor="rgba(255, 184, 0, 0.1)", line_width=0, annotation_text="Warning Zone", annotation_position="top left")
    fig.add_hrect(y0=threshold, y1=max(threshold * 1.5, history_df['Count'].max() + 10), fillcolor="rgba(255, 68, 68, 0.1)", line_width=0, annotation_text="Danger Zone", annotation_position="top left")
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.03)',
        font=dict(color='#E8E8E8', family='Inter'),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)', title='Time'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)', title='People Count'),
        hovermode='x unified',
        showlegend=False,
        height=350
    )
    return fig

# --- 🎯 Density Heatmap Visualization ---
def create_density_heatmap(count, threshold):
    density_percent = min(150, (count / threshold) * 100) 
    
    if density_percent < 70:
        color, status = '#00FF88', 'SAFE'
    elif density_percent <= 100:
        color, status = '#FFB800', 'CAUTION'
    else:
        color, status = '#FF4444', 'CRITICAL'
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=density_percent,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"<b>{status}</b>", 'font': {'size': 20, 'color': color}},
        number={'suffix': "%", 'font': {'size': 32, 'color': color}},
        gauge={
            'axis': {'range': [None, 150], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 70], 'color': 'rgba(0, 255, 136, 0.2)'},
                {'range': [70, 100], 'color': 'rgba(255, 184, 0, 0.2)'},
                {'range': [100, 150], 'color': 'rgba(255, 68, 68, 0.2)'}
            ],
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 100}
        }
    ))
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Inter"}, height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# --- Initialize Session State ---
if 'history' not in st.session_state: st.session_state.history = pd.DataFrame(columns=['Time', 'Count'])
if 'total_detected' not in st.session_state: st.session_state.total_detected = 0
if 'peak_count' not in st.session_state: st.session_state.peak_count = 0
if 'alert_count' not in st.session_state: st.session_state.alert_count = 0
if 'system_uptime' not in st.session_state: st.session_state.system_uptime = time.time()

# --- Load YOLO with optimization ---
@st.cache_resource
def load_model():
    model = YOLO('models/yolov8n.pt') 
    model.fuse() 
    return model

model = load_model()

# --- Professional Sidebar ---
st.sidebar.markdown("## ⚙️ System Configuration")
st.sidebar.markdown("---")

with st.sidebar.expander("🎛️ Detection Settings", expanded=True):
    threshold = st.slider("🚨 Crowd Threshold", 5, 100, 20, help="Maximum safe crowd capacity")
    confidence = st.slider("🎯 Detection Confidence", 0.3, 0.9, 0.45, 0.05, help="Higher = fewer false positives")
    proximity_threshold = st.slider("📏 Proximity Alert (px)", 50, 200, 120, help="Minimum safe distance between people")

st.sidebar.markdown("---")
run_camera = st.sidebar.toggle("▶️ Start Surveillance System", help="Begin real-time monitoring")

# System Stats
st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 System Statistics")
uptime_seconds = int(time.time() - st.session_state.system_uptime)
st.sidebar.metric("⏱️ Uptime", f"{uptime_seconds // 60}m {uptime_seconds % 60}s")
st.sidebar.metric("📊 Peak Count", st.session_state.peak_count)
st.sidebar.metric("⚠️ Alerts Triggered", st.session_state.alert_count)

st.markdown("---")

# --- Top Metrics Row ---
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
count_metric = metric_col1.empty()
risk_metric = metric_col2.empty()
trend_metric = metric_col3.empty()
density_metric = metric_col4.empty()

st.markdown("---")

# --- Camera Feeds Section ---
st.markdown("### 📹 Live Surveillance Feeds")
cam1_col, cam2_col = st.columns(2)
with cam1_col:
    cam1_placeholder = st.empty()
with cam2_col:
    cam2_placeholder = st.empty()

st.markdown("---")

# --- Analytics Section ---
analytics_col1, analytics_col2 = st.columns([2, 1])
with analytics_col1:
    st.markdown("### 📊 Crowd Trend Analysis")
    chart_placeholder = st.empty()
with analytics_col2:
    st.markdown("### 🎯 Density Monitor")
    density_placeholder = st.empty()

st.markdown("---")

# --- Alert Section ---
st.markdown("### 🚨 System Status & AI Logs")
alert_placeholder = st.empty()

# ---------------------------------------------------------
# 🔴 Main Loop: Optimized Performance Mode
# ---------------------------------------------------------
if run_camera:
    cap1 = cv2.VideoCapture(0)
    cap1.set(cv2.CAP_PROP_BUFFERSIZE, 1)  

    frame_counter, last_chart_update, last_density_update = 0, 0, 0
    
    while run_camera:
        ret1, frame1 = cap1.read()
            
        if not ret1:
            st.error("❌ No active cameras found!")
            break
            
        frame_counter += 1
        if frame_counter % 2 != 0: continue # 🏎️ Process every 2nd frame

        # --- 🧠 Process Cam 1 ---
        frame1 = cv2.resize(frame1, (640, 480))
        res1 = model(frame1, classes=[0], conf=confidence, imgsz=320, verbose=False)
        count1 = len(res1[0].boxes)
        cam1_placeholder.image(res1[0].plot(), channels="BGR", use_container_width=True)
        
        # Risk/Proximity checking
        boxes1 = res1[0].boxes.xyxy.cpu().numpy()
        risky_people = check_proximity_violations(boxes1, distance_threshold=proximity_threshold) if count1 > 1 else 0

        # --- 📊 Unified Analytics ---
        total_count = count1 
        st.session_state.total_detected += total_count
        st.session_state.peak_count = max(st.session_state.peak_count, total_count)
        
        density_percent = min(150, (total_count / threshold) * 100)
        
        # 💡 AI Prediction
        prediction = get_crowd_prediction(st.session_state.history) if not st.session_state.history.empty else "Analyzing..."
        
        # UI Metric Updates
        count_metric.metric("👥 Current Count", total_count, delta=f"{total_count - threshold} vs limit", delta_color="inverse")
        risk_metric.metric("⚠️ Proximity Alerts", risky_people, delta="High Risk" if risky_people > 3 else "Normal", delta_color="inverse")
        trend_metric.metric("🔮 AI Prediction", prediction)
        density_metric.metric("📊 Density", f"{int(density_percent)}%", delta="Critical" if density_percent >= 100 else "Optimal", delta_color="inverse")
        
        # Update Data History
        now = datetime.now().strftime("%H:%M:%S")
        st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame({'Time': [now], 'Count': [total_count]})]).tail(30)
        
        # 📈 Throttled UI Rendering
        current_time = time.time()
        if current_time - last_chart_update > 1.0:
            chart_placeholder.plotly_chart(
                create_dynamic_chart(st.session_state.history, threshold), 
                use_container_width=True,
                key=f"trend_chart_{frame_counter}"  # <-- ही लाईन ॲड केली
            )
            last_chart_update = current_time
            
        if current_time - last_density_update > 1.5:
            density_placeholder.plotly_chart(
                create_density_heatmap(total_count, threshold), 
                use_container_width=True,
                key=f"density_chart_{frame_counter}" # <-- ही लाईन ॲड केली
            )
            last_density_update = current_time
        
        # --- 🚨 AI Alerts Logic ---
        if 'last_alert_time' not in st.session_state: st.session_state.last_alert_time = 0
        
        if total_count > threshold or risky_people > 3:
            st.session_state.alert_count += 1
            if (current_time - st.session_state.last_alert_time) > 15:
                msg, status = get_smart_alert(total_count, threshold, risky_people)
                st.session_state.last_alert_msg, st.session_state.last_alert_status = msg, status
                st.session_state.last_alert_time = current_time
                speak_warning("Attention! Area capacity exceeded. Please maintain distance.")
                
            if 'last_alert_msg' in st.session_state:
                if st.session_state.last_alert_status == "CRITICAL" or st.session_state.last_alert_status == "danger": 
                    alert_placeholder.error(f"🚨 **CRITICAL ALERT:** {st.session_state.last_alert_msg}")
                else: 
                    alert_placeholder.warning(f"⚠️ **WARNING:** {st.session_state.last_alert_msg}")
        else:
            alert_placeholder.success("✅ **System Status:** All Clear - Crowd within safe limits")

    cap1.release()

# --- 📄 Professional Report Generation ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 📄 Post-Event Analytics")
if not run_camera:
    if st.sidebar.button("📊 Generate Incident Report", use_container_width=True):
        with st.spinner("🔄 Generating AI-powered Safety Audit..."):
            peak_c = int(st.session_state.history['Count'].max()) if not st.session_state.history.empty else 0
            pdf_path = create_safety_report(peak_c, st.session_state.alert_count)
            with open(pdf_path, "rb") as f:
                st.sidebar.download_button("📥 Download Official PDF", f, file_name=pdf_path, mime="application/pdf", use_container_width=True)
            st.sidebar.success("✅ Report generated!")