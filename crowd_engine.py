import cv2
from ultralytics import YOLO

# मॉडेल लोड करणे (models फोल्डरमध्ये yolov8n.pt असावे)
model = YOLO('models/yolov8n.pt') 

def process_frame(frame):
    # केवळ 'person' (class 0) शोधण्यासाठी
    results = model(frame, classes=[0], conf=0.5)
    
    # माणसांची संख्या मोजणे
    count = len(results[0].boxes)
    
    # फोटोवर boxes काढणे
    annotated_frame = results[0].plot()
    
    return annotated_frame, count