import pandas as pd
import numpy as np

def get_crowd_prediction(history_df):
    """
    Analyzes the recent crowd history to predict the immediate trend.
    Uses Moving Averages to determine if the crowd is growing or shrinking.
    """
    # जर डेटा खूप कमी असेल, तर सिस्टिमला थोडा वेळ द्या
    if history_df is None or len(history_df) < 6:
        return "Gathering Data ⏳"
        
    # 'Count' कॉलमचा डेटा घ्या
    counts = history_df['Count'].tolist()
    
    # जुना डेटा आणि नवीन डेटा यांची सरासरी (Average) काढा
    mid = len(counts) // 2
    older_avg = np.mean(counts[:mid])
    recent_avg = np.mean(counts[mid:])
    
    # गर्दी वाढण्याचा किंवा कमी होण्याचा वेग (Rate of Change)
    diff = recent_avg - older_avg
    
    # लॉजिक: डॅशबोर्डवर दाखवण्यासाठी अचूक दिशा
    if diff > 2.5:
        return "Rising Quickly 📈"
    elif diff > 0.5:
        return "Slowly Increasing ↗️"
    elif diff < -2.5:
        return "Clearing Fast 📉"
    elif diff < -0.5:
        return "Slowly Decreasing ↘️"
    else:
        return "Stable ➡️"

# Local Testing
if __name__ == "__main__":
    print("Testing Predictor Module...")
    # डमी डेटा: गर्दी 10 वरून 25 पर्यंत वाढत आहे
    dummy_data = pd.DataFrame({'Count': [10, 12, 15, 18, 22, 25]})
    prediction = get_crowd_prediction(dummy_data)
    print(f"Data: {dummy_data['Count'].tolist()}")
    print(f"AI Prediction: {prediction}")