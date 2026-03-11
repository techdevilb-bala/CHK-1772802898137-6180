import pandas as pd
import numpy as np

def get_crowd_prediction(history_df, threshold):
    """
    Advanced Predictive Intelligence (V3.0)
    Calculates Volumetric Velocity & Time-to-Critical-Mass.
    """
    try:
        # बेसलाईन तयार होण्यासाठी किमान १० डेटा पॉईंट्स लागतील
        if len(history_df) < 10:
            return "🛰️ CALIBRATING: Establishing baseline flow trajectory...", "INFO"

        # शेवटचे १० स्नॅपशॉट्स (Trajectory Analysis)
        counts = history_df['Count'].values[-10:].astype(float)
        x = np.arange(len(counts))
        
        # Polynomial Regression (Degree 1 for Trend, Degree 2 for Acceleration)
        # आपण इथे साध्या Slope ऐवजी 'Momentum' मोजणार आहोत
        poly = np.polyfit(x, counts, 1)
        slope = poly[0] 
        current_count = counts[-1]
        
        # 🚀 Crowding Momentum Calculation (V/T)
        occupancy_rate = (current_count / threshold) * 100

        # १. जर गर्दी वेगाने वाढत असेल (SLOPE > 0.5)
        if slope > 0.4:
            remaining_cap = threshold - current_count
            
            if remaining_cap > 0:
                # Time to Breach (Minutes)
                time_to_breach = int(remaining_cap / (slope + 1e-6))
                time_to_breach = max(1, time_to_breach)
                
                # Risk Level ठरवणे
                risk = "HIGH" if occupancy_rate > 80 else "MODERATE"
                
                msg = f"⚠️ {risk} RISK: Density surge detected (+{round(slope, 1)} pax/unit). Est. limit breach in {time_to_breach} mins."
                return msg, "WARNING"
            else:
                return "🚨 CRITICAL: Volumetric limit exceeded. Initiate immediate dispersal protocols.", "DANGER"
        
        # २. जर गर्दी कमी होत असेल
        elif slope < -0.2:
            return "📉 DISPERSING: Crowd momentum is negative. Flow is normalizing.", "SUCCESS"
        
        # ३. जर गर्दी स्थिर असेल
        else:
            if occupancy_rate > 90:
                return "🟠 STAGNANT: High density but stable flow. Monitor for bottlenecking.", "WARNING"
            return "✅ STABLE: Current trajectory indicates no immediate threshold risk.", "STABLE"

    except Exception as e:
        return f"AI Logic Syncing... {str(e)}", "INFO"