import numpy as np

def get_crowd_prediction(history_df):
    """
    Uses Linear Regression to predict future crowd size based on recent history.
    """
    # We need at least 10 data points to find a trend
    if len(history_df) < 10:
        return "Gathering data..."
        
    # Get the crowd counts as Y-axis, and time steps as X-axis
   # Get the crowd counts as Y-axis, and time steps as X-axis
    y = np.array(history_df['Count'].values, dtype=float)  # 🟢 FIX: Convert to Float
    x = np.arange(len(y))
    
    # Apply Linear Regression (y = mx + c)
    # slope (m) tells us if crowd is increasing or decreasing
    slope, intercept = np.polyfit(x, y, 1)
    
    # Predict crowd size for the next 15 time steps
    future_x = len(y) + 15
    predicted_crowd = int((slope * future_x) + intercept)
    
    # Crowd cannot be negative
    predicted_crowd = max(0, predicted_crowd)
    
    # Determine the trend status
    if slope > 0.3:
        return f"📈 Rising! Next: ~{predicted_crowd}"
    elif slope < -0.3:
        return f"📉 Clearing. Next: ~{predicted_crowd}"
    else:
        return f"➡️ Stable. Next: ~{predicted_crowd}"

# Local Testing
if __name__ == "__main__":
    import pandas as pd
    dummy_data = pd.DataFrame({'Count': [5, 6, 8, 10, 12, 15, 18, 20, 22, 25]})
    print("Prediction Test:", get_crowd_prediction(dummy_data))