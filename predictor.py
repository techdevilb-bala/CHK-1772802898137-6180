import pandas as pd
import google.generativeai as genai

# जर तुझ्याकडे Gemini API Key असेल तर इथे टाक (नसले तरीही सिस्टीम 'Offline Failsafe' लॉजिकवर चालेल)
GEMINI_API_KEY = "इथे_तुझी_API_KEY_टाक" 

def get_crowd_prediction(history_df):
    if len(history_df) < 5:
        return "Gathering Data..."

    # Layer 2: Offline Edge Logic (जर इंटरनेट/API नसेल तर)
    recent_counts = history_df['Count'].tolist()
    growth_rate = recent_counts[-1] - recent_counts[0]
    
    offline_prediction = "Stable Flow 🟢"
    if growth_rate > 15:
        offline_prediction = "High Stampede Risk! (Surge) 🔴"
    elif growth_rate > 5:
        offline_prediction = "Moderate Risk (Crowd Growing) 🟡"

    # Layer 1: Gemini Cloud Logic (AI Analysis)
    try:
        if GEMINI_API_KEY != "इथे_तुझी_API_KEY_टाक":
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Crowd counts over last few seconds: {recent_counts}. Based on this trend, predict stampede risk in 5 words."
            response = model.generate_content(prompt)
            return response.text.strip()
    except:
        pass # इंटरनेट नसेल तर Offline Edge Logic चालेल

    return offline_prediction