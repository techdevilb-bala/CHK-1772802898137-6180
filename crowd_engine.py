import cv2
from ultralytics import YOLO

class CrowdAnalyzer:
    def __init__(self):
        # मॉडेल लोड करणे
        self.model = YOLO('yolov8n.pt') 
        
    def count_people(self, frame):
        # फक्त लोक डिटेक्ट करणे
        results = self.model(frame, classes=[0], conf=0.4, verbose=False)
        count = len(results[0].boxes)
        annotated_frame = results[0].plot()
        return count, annotated_frame

def run_test():
    analyzer = CrowdAnalyzer()
    cap = None
    
    # कॅमेरा शोधण्यासाठी लूप (०, १, २ किंवा -१ तपासेल)
   # सुधारित लूप
    for index in [0, 1, 2, 700]: # कधीकधी इंडेक्स मोठा असतो
        temp_cap = cv2.VideoCapture(index) # इथे CAP_DSHOW काढला आहे
        if temp_cap.isOpened():
            cap = temp_cap
            print(f"Success: Camera found at index {index}")
            break
        temp_cap.release()
    if cap is None:
        print("Error: कॅमेरा सापडला नाही!")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        count, img = analyzer.count_people(frame)
        cv2.putText(img, f"People: {count}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Crowd Engine Test", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_test()