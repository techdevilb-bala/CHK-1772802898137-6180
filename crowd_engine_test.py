import cv2
from ultralytics import YOLO

class CrowdAnalyzer:
    def __init__(self):
        print("Loading YOLO Model...")
        self.model = YOLO('yolov8n.pt') 
        
    def count_people(self, frame):
        # फक्त लोक (class 0) डिटेक्ट करणे
        results = self.model(frame, classes=[0], conf=0.4, verbose=False)
        count = len(results[0].boxes)
        annotated_frame = results[0].plot()
        return count, annotated_frame

def run_test():
    analyzer = CrowdAnalyzer()
    cap = None
    
    print("Searching for active cameras...")
    # कॅमेरा शोधण्यासाठी लूप (Webcam, USB Cam, IP Cam)
    for index in [0, 1, 2, 700]: 
        temp_cap = cv2.VideoCapture(index)
        if temp_cap.isOpened():
            cap = temp_cap
            print(f"✅ Success: Camera found at index {index}")
            break
        temp_cap.release()
        
    if cap is None:
        print("❌ Error: कॅमेरा सापडला नाही! कृपया USB किंवा IP तपासा.")
        return

    print("Press 'q' to exit the test window.")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: 
            print("Frame dropped.")
            break
        
        # फ्रेम रिसाईज करा म्हणजे लॅग येणार नाही
        frame = cv2.resize(frame, (640, 480))
        count, img = analyzer.count_people(frame)
        
        # स्क्रीनवर माहिती दाखवणे
        cv2.putText(img, f"Live Count: {count}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Hardware Diagnostic - Crowd Engine", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_test()