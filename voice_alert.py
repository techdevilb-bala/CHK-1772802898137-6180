import pyttsx3
import threading

def speak_warning(message):
    """
    हे फंक्शन कॅमेरा फीड न थांबवता बॅकग्राउंडमध्ये आवाज देईल.
    """
    def run_speech():
        try:
            engine = pyttsx3.init()
            # आवाजाचा स्पीड (Rate) आणि व्हॉल्युम सेट करा
            engine.setProperty('rate', 150) 
            engine.setProperty('volume', 1.0)
            engine.say(message)
            engine.runAndWait()
        except Exception as e:
            print(f"Voice Alert Error: {e}")

    # Threading मुळे तुझा कॅमेरा लॅग होणार नाही!
    thread = threading.Thread(target=run_speech)
    thread.start()