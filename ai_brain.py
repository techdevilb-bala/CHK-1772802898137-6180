def get_smart_alert(total_count, threshold, risky_people):
    
    """
    गर्दी आणि धोक्याच्या पातळीनुसार स्मार्ट मेसेज बनवणे.
    """
    if risky_people > 5:
        # जर खूप लोक एकमेकांच्या जवळ आले असतील (Stampede Risk)
        msg = f"STAMPEDE WARNING: {risky_people} people are in critical proximity! Deploy digital barricades."
        status = "CRITICAL"
    elif total_count > threshold:
        # जर फक्त गर्दी वाढली असेल
        msg = f"OVERCROWDING DETECTED: Zone capacity exceeded by {total_count - threshold} people."
        status = "danger"
    else:
        # सगळं नॉर्मल असेल
        msg = "Safe Operations: Crowd flow is normal."
        status = "success"
        
    return msg, status
def get_smart_alert(current_count, threshold, running_detected=False):
    """Generates tactical decisions based on AI analysis."""
    
    # जर पळापळ (Panic) दिसत असेल
    if running_detected:
        return "PANIC DETECTED: Deploy Quick Response Team (QRT) to Sector A.", "CRITICAL"
    
    # जर गर्दी क्षमतेच्या बाहेर गेली असेल
    occupancy = (current_count / threshold) * 100
    
    if occupancy > 100:
        return f"CRITICAL OVERLOAD ({int(occupancy)}%): Halt all entries immediately. Open Exit B.", "danger"
    elif occupancy > 80:
        return f"WARNING ({int(occupancy)}%): Deploy staff to Entry Zone for flow throttling.", "warning"
    else:
        return "Operations Normal. Monitoring stable flow.", "safe"