import cv2
import numpy as np

def draw_and_count_zone(frame, boxes, zone_coords, zone_name="Restricted Area", limit=3):
    """
    कॅमेरा फ्रेमवर एक वर्चुअल झोन बनवतो आणि त्या झोनच्या आत किती लोक आहेत ते मोजतो.
    """
    # Convert coordinates to numpy array for OpenCV
    zone_pts = np.array(zone_coords, np.int32)
    zone_pts = zone_pts.reshape((-1, 1, 2))
    
    zone_count = 0
    
    # प्रत्येक माणसाचा सेंटर पॉईंट (cx, cy) काढा
    for box in boxes:
        cx = int((box[0] + box[2]) / 2)
        cy = int((box[1] + box[3]) / 2)
        
        # Point Polygon Test: चेक करा की माणूस त्या झोनच्या आत आहे का?
        is_inside = cv2.pointPolygonTest(zone_pts, (cx, cy), False)
        
        if is_inside >= 0:
            zone_count += 1
            # माणूस झोनमध्ये असेल तर त्याच्या अंगावर लाल डॉट दाखवा
            cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1) 
            
    # जर गर्दी लिमिटपेक्षा जास्त असेल तर झोन लाल करा, नाहीतर हिरवा ठेवा (Neon Colors)
    color = (0, 0, 255) if zone_count >= limit else (0, 255, 0) 
    
    # झोनची बॉर्डर (Virtual Fence) काढा
    cv2.polylines(frame, [zone_pts], isClosed=True, color=color, thickness=3)
    
    # झोनचे नाव आणि गर्दीचा आकडा फ्रेमवर लिहा
    text = f"{zone_name}: {zone_count} / {limit}"
    cv2.putText(frame, text, (zone_coords[0][0], zone_coords[0][1] - 15), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
    return frame, zone_count