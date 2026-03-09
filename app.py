import pandas as pd
from datetime import datetime
import time

import streamlit as st
import cv2
from ultralytics import YOLO
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Team Modules Import ---
from report_gen import create_safety_report
from safety_math import check_proximity_violations

# 1. Setup Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Smart Crowd Intelligence", layout="wide")
st.title("🛡️ Smart Crowd Intelligence & AI Alerts")

# Initialize data history
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Time', 'Count'])

# Load YOLOv8
@st.cache_resource
def load_model():
    return YOLO('models/yolov8n.pt')
model = load_model()

# Sidebar Configuration
st.sidebar.header("Control Panel")
threshold = st.sidebar.slider("Crowd Limit", 5, 50, 10)
run_camera = st.sidebar.toggle("Start Surveillance")

# UI Placeholders
col1, col2 = st.columns([2, 1])
with col1:
    frame_placeholder = st.empty()
with col2:
    chart_placeholder = st.empty()
    alert_placeholder = st.empty()

# UI Metrics
metric_col1, metric_col2 = st.sidebar.columns(2)
count_metric = metric_col1.empty()
risk_metric = metric_col2.empty()

# Main Loop
if run_camera:
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        # AI Detection
        results = model(frame, classes=[0], conf=0.5, verbose=False)
        current_count = len(results[0].boxes)
        
        # --- NEW: Proximity Math ---
        boxes = results[0].boxes.xyxy.cpu().numpy() # Get raw coordinates
        risky_people = check_proximity_violations(boxes, distance_threshold=150)
        
        # Update chart data
        now = datetime.now().strftime("%H:%M:%S")
        new_row = pd.DataFrame({'Time': [now], 'Count': [current_count]})
        st.session_state.history = pd.concat([st.session_state.history, new_row]).tail(20)
        
        # Display Results
        chart_placeholder.line_chart(st.session_state.history.set_index('Time'))
        frame_placeholder.image(results[0].plot(), channels="BGR")
        
        # Update Dashboard Metrics
        count_metric.metric("Total People", current_count)
        risk_metric.metric("⚠️ High Risk", risky_people)

        # Gemini AI Alert
       # --- NEW: Gemini AI Alert with Cooldown (Speed Fix) ---
        if 'last_alert_time' not in st.session_state:
            st.session_state.last_alert_time = 0

        current_time_sec = time.time()
        
        if current_count > threshold or risky_people > 2:
            # १५ सेकंदांचा Cooldown (म्हणजे AI सारखा सारखा कॉल होणार नाही)
            if (current_time_sec - st.session_state.last_alert_time) > 15:
                prompt = f"Crowd count: {current_count}. People standing too close: {risky_people}. Give a short urgent safety warning in Marathi and English."
                try:
                    response = gemini_model.generate_content(prompt)
                    st.session_state.last_alert_msg = response.text
                    st.session_state.last_alert_time = current_time_sec
                except Exception as e:
                    st.session_state.last_alert_msg = "AI system busy... Please wait."
            
            # Show the saved alert message without slowing down the camera
            if 'last_alert_msg' in st.session_state:
                alert_placeholder.error(f"🚨 AI ALERT:\n{st.session_state.last_alert_msg}")
        else:
            alert_placeholder.success("Crowd is within safe limits. Proper distancing maintained.")
## --- NEW: PDF Report Generator (Safe Mode) ---
st.sidebar.markdown("---")
st.sidebar.subheader("📄 Daily Safety Report")

# Rule: Camera must be off to generate report safely
if run_camera:
    st.sidebar.warning("⚠️ Please turn OFF 'Start Surveillance' to download the report.")
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