import pyttsx3
import threading
import pyttsx3
import threading

def speak_warning(text):
    """Localized Voice Protocol with Thread Safety"""
    def run_speech():
        try:
            # नवीन इंजिन सुरू करणे
            engine = pyttsx3.init()
            
            # आवाजाचा वेग (Rate) आणि स्पष्टता
            engine.setProperty('rate', 160)
            engine.setProperty('volume', 1.0)
            
            # बोलणे सुरू करणे
            engine.say(text)
            engine.runAndWait()
            
            # इंजिन पूर्णपणे थांबवणे (महत्त्वाचे आहे!)
            engine.stop()
            del engine # मेमरी फ्री करणे
        except Exception as e:
            print(f"Voice Alert Error: {e}")

    # डॅशबोर्ड लॅग होऊ नये म्हणून थ्रेडमध्ये चालवा
    thread = threading.Thread(target=run_speech, daemon=True)
    thread.start()

if __name__ == "__main__":
    # टेस्ट करण्यासाठी
    speak_warning("सिस्टम सुरू झाली आहे. गर्दीवर लक्ष ठेवा.")
def speak_warning(text):
    def run_speech():
        try:
            # नवीन इंजिन दरवेळी सुरू करणे चांगले असते
            engine = pyttsx3.init()
            
            # आवाजाचा वेग आणि वॉल्यूम सेट करा
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)
            
            # मराठी किंवा हिंदी आवाजासाठी (जर लॅपटॉपमध्ये असेल तर)
            voices = engine.getProperty('voices')
            # engine.setProperty('voice', voices[1].id) 

            engine.say(text)
            engine.runAndWait()
            # इंजिन थांबवणे महत्त्वाचे आहे
            engine.stop()
        except Exception as e:
            print(f"Speech Error: {e}")

    # हे थ्रेडमध्ये चालवा जेणेकरून कॅमेरा अडकणार नाही
    threading.Thread(target=run_speech, daemon=True).start()