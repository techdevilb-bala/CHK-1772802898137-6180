import csv
from datetime import datetime
import os

def log_crowd_data(count):
    """
    लोकांची संख्या आणि वेळ 'crowd_report.csv' मध्ये सेव्ह करते.
    """
    filename = "crowd_report.csv"
    
    # फाईल आधीपासून आहे का ते तपासणे (हेडिंग टाकण्यासाठी)
    file_exists = os.path.isfile(filename)
    
    # सध्याची तारीख आणि वेळ
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # 'a' (append) मोडमध्ये फाईल उघडणे जेणेकरून जुना डेटा पुसला जाणार नाही
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # जर फाईल नवीन असेल तर पहिल्या ओळीत कॉलमची नावे टाका
            if not file_exists:
                writer.writerow(['Timestamp', 'Person Count'])
            
            # डेटा लिहिणे
            writer.writerow([now, count])
        
        print(f"✅ डेटा सेव्ह झाला: {now} | Count: {count}")
        return True
    except Exception as e:
        print(f"❌ CSV Error: {e}")
        return False

# ही फाईल स्वतंत्रपणे टेस्ट करण्यासाठी (optional)
if __name__ == "__main__":
    log_crowd_data(10) # १० लोकांचा डमी डेटा टाकून टेस्ट करणे