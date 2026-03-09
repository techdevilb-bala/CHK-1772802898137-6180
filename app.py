from report_gen import create_safety_report
import pandas as pd
from datetime import datetime
import streamlit as st
import cv2
from ultralytics import YOLO
import google.generativeai as genai
import os
from dotenv import load_dotenv


# 1. Setup Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🛡️ Smart Crowd Intelligence & AI Alerts")
# Initialize data history
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Time', 'Count'])

# Placeholder for the chart
chart_placeholder = st.empty()

# Load YOLOv8
model = YOLO('models/yolov8n.pt') 

# Sidebar Configuration
threshold = st.sidebar.slider("Crowd Limit", 5, 50, 10)
# --- PDF Report Integration ---
st.sidebar.markdown("---")
if st.sidebar.button("📄 Generate Daily Report"):
    # Calculate peak crowd from your session history
    peak_crowd = int(st.session_state.history['Count'].max()) if not st.session_state.history.empty else 0
    
    # Generate the PDF using your friend's function
    pdf_filename = create_safety_report(max_crowd=peak_crowd, alerts_triggered=3)
    
    # Provide the download link
    with open(pdf_filename, "rb") as pdf_file:
        st.sidebar.download_button(
            label="⬇️ Download PDF Now",
            data=pdf_file,
            file_name=pdf_filename,
            mime="application/pdf"
        )
run_camera = st.sidebar.toggle("Start Surveillance")
frame_placeholder = st.empty()
alert_placeholder = st.empty()

if run_camera:
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        results = model(frame, classes=[0], conf=0.5, verbose=False)
        current_count = len(results[0].boxes)
        # Update chart data
        now = datetime.now().strftime("%H:%M:%S")
        new_row = pd.DataFrame({'Time': [now], 'Count': [current_count]})
        
        # Keep only the last 20 data points for performance
        st.session_state.history = pd.concat([st.session_state.history, new_row]).tail(20)
        
        # Display the chart
        chart_placeholder.line_chart(st.session_state.history.set_index('Time'))
        # Display Results
        frame_placeholder.image(results[0].plot(), channels="BGR")
        st.sidebar.metric("People Count", current_count)

        # 2. Trigger Gemini AI Alert
        if current_count > threshold:
            prompt = f"Crowd count is {current_count}. Limit is {threshold}. Give a short urgent safety warning in Marathi and English."
            try:
                response = gemini_model.generate_content(prompt)
                alert_placeholder.error(f"🚨 AI ALERT:\n{response.text}")
            except Exception as e:
                alert_placeholder.warning("AI system busy...")
        else:
            alert_placeholder.success("Crowd is within safe limits.")

        if not run_camera: break
    cap.release()