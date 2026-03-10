import pyttsx3
import threading

def speak_warning(text):
    """
    ही फंक्शन बॅकग्राउंडमध्ये (वेगळ्या थ्रेडवर) आवाज देईल, 
    जेणेकरून आपला मुख्य कॅमेरा आणि YOLO चा व्हिडिओ स्लो होणार नाही.
    """
    def run_speech():
        try:
            engine = pyttsx3.init()
            # आवाजाचा स्पीड (Rate) आणि आवाज (Volume) सेट करणे
            engine.setProperty('rate', 160)  
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Audio Error: {e}")

    # Background Thread चालू करा
    audio_thread = threading.Thread(target=run_speech, daemon=True)
    audio_thread.start()

# Local Testing
if __name__ == "__main__":
    speak_warning("System testing. Voice alert is active.")