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

# Load YOLOv8
model = YOLO('models/yolov8n.pt') 

# Sidebar Configuration
threshold = st.sidebar.slider("Crowd Limit", 5, 50, 10)
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