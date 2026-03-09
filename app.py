import cv2
from ultralytics import YOLO
from flask import Flask, Response
import datetime

# -------------------------
# Load YOLO Model
# -------------------------
model = YOLO("yolov8n.pt")

# -------------------------
# Flask App
# -------------------------
app = Flask(__name__)

# -------------------------
# Camera Setup
# -------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not found")
    exit()

print("✅ Camera Started")

# -------------------------
# Crowd Detection Function
# -------------------------
def generate_frames():
    while True:

        success, frame = cap.read()
        if not success:
            break

        # YOLO Detection
        results = model(frame)

        count = 0

        for r in results:
            boxes = r.boxes

            for box in boxes:
                cls = int(box.cls[0])

                # Class 0 = person
                if cls == 0:
                    count += 1

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),2)
                    cv2.putText(frame,"Person",(x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)

        # Crowd Count Display
        cv2.putText(frame,f"People Count: {count}",
        (20,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

        # Save log
        now = datetime.datetime.now()
        print(f"📊 {now} | Crowd Count: {count}")

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# -------------------------
# Flask Routes
# -------------------------
@app.route('/')
def home():
    return """
    <h1>Smart Crowd Intelligence</h1>
    <img src="/video_feed" width="800">
    """

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
    mimetype='multipart/x-mixed-replace; boundary=frame')

# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)