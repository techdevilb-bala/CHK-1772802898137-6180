import numpy as np

def check_proximity_violations(boxes, distance_threshold=120):
    """
    Calculates how many people are violating the proximity rule (social distancing).
    Uses fast NumPy array operations to prevent video lag.
    """
    num_people = len(boxes)
    
    # जर 1 पेक्षा कमी लोक असतील, तर डिस्टन्स मोजण्याची गरजच नाही
    if num_people < 2:
        return 0
        
    # सर्व लोकांचे Centroids (मध्यबिंदू) वेगाने काढणे
    centroids = []
    for box in boxes:
        x1, y1, x2, y2 = box[:4]
        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0
        centroids.append([cx, cy])
        
    centroids = np.array(centroids)
    risky_indices = set()
    
    # Pairwise Distance Calculation (हाय-स्पीड लूप)
    for i in range(num_people):
        for j in range(i + 1, num_people):
            # Euclidean distance formula
            dist = np.linalg.norm(centroids[i] - centroids[j])
            
            if dist < distance_threshold:
                risky_indices.add(i)
                risky_indices.add(j)
                
    # किती लोक एकमेकांच्या खूप जवळ उभे आहेत त्याचा आकडा परत करा
    return len(risky_indices)

# Local Testing
if __name__ == "__main__":
    # Dummy boxes [x1, y1, x2, y2]
    test_boxes = np.array([
        [10, 10, 50, 100],  # Person 1 (Close to Person 2)
        [20, 20, 60, 110],  # Person 2 (Close to Person 1)
        [300, 300, 350, 400] # Person 3 (Far away)
    ])
    
    violations = check_proximity_violations(test_boxes, distance_threshold=100)
    print(f"Test Run: Detected {violations} risky people.")