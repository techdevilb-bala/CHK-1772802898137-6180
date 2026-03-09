import streamlit as st
import cv2
from ultralytics import YOLO

st.title("🛡️ Smart Crowd Intelligence: Live Tracking")

# 1. Load the YOLOv8 Model
# Make sure 'yolov8n.pt' is in your 'models/' folder
model = YOLO('models/yolov8n.pt') 

run_camera = st.sidebar.toggle("Start Surveillance")
frame_placeholder = st.empty()

if run_camera:
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Camera access failed!")
            break
        
        # 2. Run Detection (Class 0 is 'person')
        results = model(frame, classes=[0], conf=0.5, verbose=False)
        
        # 3. Get Count and Annotated Frame
        current_count = len(results[0].boxes)
        annotated_frame = results[0].plot()

        # 4. Display Result
        st.sidebar.metric("People Count", current_count)
        frame_placeholder.image(annotated_frame, channels="BGR")

        if not run_camera:
            break
    cap.release()