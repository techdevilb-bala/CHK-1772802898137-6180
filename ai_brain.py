import pyttsx3
import threading
from google import genai
import ollama
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Client (New SDK)
try:
    gemini_client = genai.Client(api_key=api_key) if api_key else None
except Exception:
    gemini_client = None

# --- 🔊 Audio System (100% Offline Background Thread) ---
def speak_alert(text):
    def run_speech():
        try:
            engine = pyttsx3.init()
            rate = engine.getProperty('rate')
            engine.setProperty('rate', rate - 30) 
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Audio Error: {e}")
            
    # Run in background so video doesn't lag
    threading.Thread(target=run_speech, daemon=True).start()

# --- 🧠 The 3-Tier AI Engine ---
def get_smart_alert(current_count, threshold, risky_people):
    # Condition 1: Everything is Safe
    if current_count <= threshold and risky_people <= 2:
        return "✅ Safe: Crowd is within normal limits. Proper distancing maintained.", "safe"

    prompt = f"Crowd limit is {threshold}, but current count is {current_count}. {risky_people} people are standing too close. Give a strict, short emergency warning in English."

    # 🌐 TIER 1: Cloud AI (Gemini Flash - High IQ)
    if gemini_client:
        try:
            response = gemini_client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            speak_alert("Warning! Cloud AI has detected a crowd limit violation.")
            return f"🚨 CLOUD AI (Gemini):\n{response.text}", "danger"
        except Exception as e:
            print("Gemini failed, shifting to Tier 2...")

    # 💻 TIER 2: Local Edge AI (Llama 3 via Ollama - Offline IQ)
    try:
        response = ollama.chat(model='llama3', messages=[
            {'role': 'user', 'content': prompt}
        ])
        speak_alert("Emergency! System shifted to Local AI. Crowd limit exceeded.")
        return f"⚠️ EDGE AI (Llama 3 Offline):\n{response['message']['content']}", "warning"
        
    except Exception as local_e:
        print("Ollama failed, shifting to Tier 3...")
        
        # ⚙️ TIER 3: Hardcoded Fallback Logic (Absolute worst-case)
        offline_msg = (
            f"🔴 BASIC OFFLINE ALERT:\n"
            f"Limit crossed! Current crowd: {current_count}.\n"
            f"High-risk proximity: {risky_people} people.\n"
            f"Please maintain distance immediately."
        )
        speak_alert("System operating in basic logic mode. Please maintain distance.")
        return offline_msg, "danger"

# Local Hardware testing
if __name__ == "__main__":
    print("Testing 3-Tier Brain...")
    msg, status = get_smart_alert(25, 10, 5)
    print(f"Status: {status}\nMessage: {msg}")