import requests
import threading
import urllib.parse

def send_whatsapp_alert(message, phone_number, api_key):
    """
    ही फंक्शन बॅकग्राउंडमध्ये (वेगळ्या थ्रेडवर) WhatsApp मेसेज पाठवेल, 
    जेणेकरून कॅमेराचा व्हिडिओ स्लो होणार नाही.
    """
    def send_req():
        try:
            # मेसेजला URL फॉरमॅटमध्ये कन्व्हर्ट करा (उदा. Space ऐवजी %20)
            encoded_message = urllib.parse.quote(message)
            url = f"https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={encoded_message}&apikey={api_key}"
            
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ WhatsApp Alert Sent Successfully!")
            else:
                print(f"⚠️ WhatsApp API Error: {response.text}")
        except Exception as e:
            print(f"WhatsApp Request Error: {e}")

    # Background Thread चालू करा
    wp_thread = threading.Thread(target=send_req, daemon=True)
    wp_thread.start()

# Local Testing
if __name__ == "__main__":
    # इथे तुझा स्वतःचा नंबर (Country code सह, + नको) आणि मिळालेली API Key टाकून टेस्ट कर
    send_whatsapp_alert("🚨 System Testing: Smart Crowd Intelligence Active!", "919876543210", "123456")