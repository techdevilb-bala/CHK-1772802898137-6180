import math

def calculate_distance(box1, box2):
    """
    Calculates the Euclidean distance between the center points of two bounding boxes.
    YOLO box format: [x1, y1, x2, y2]
    """
    # Find the center coordinates of Box 1
    c1_x = (box1[0] + box1[2]) / 2
    c1_y = (box1[1] + box1[3]) / 2
    
    # Find the center coordinates of Box 2
    c2_x = (box2[0] + box2[2]) / 2
    c2_y = (box2[1] + box2[3]) / 2
    
    # Apply Euclidean Distance Formula
    distance = math.sqrt((c2_x - c1_x)**2 + (c2_y - c1_y)**2)
    return distance

def check_proximity_violations(boxes, distance_threshold=100):
    """
    Takes a list of YOLO bounding boxes and returns the number of people 
    who are standing dangerously close to each other.
    """
    violations = set()
    num_people = len(boxes)
    
    # We need at least 2 people to check the distance
    if num_people < 2:
        return 0
        
    # Compare every person with every other person
    for i in range(num_people):
        for j in range(i + 1, num_people):
            dist = calculate_distance(boxes[i], boxes[j])
            
            # If distance is less than threshold, it's a violation
            if dist < distance_threshold:
                violations.add(i)
                violations.add(j)
                
    return len(violations) # Total people at risk

# Local test block
if __name__ == "__main__":
    # Dummy boxes: [x1, y1, x2, y2]
    test_boxes = [[10, 10, 50, 50], [15, 15, 55, 55], [300, 300, 350, 350]]
    risky_people = check_proximity_violations(test_boxes, distance_threshold=100)
    print(f"Test Run: {risky_people} people are standing too close!")