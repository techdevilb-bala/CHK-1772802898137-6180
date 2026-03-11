import requests
from requests.auth import HTTPBasicAuth

# ⚠️ इथे तुझे खरे डिटेल्स टाक
account_sid = 'ACf0ec2706c55ce3e04a3e4679d8919920'
auth_token = '28bf9a7b02484292b2bc76f903f97084'
from_wa = 'whatsapp:+14155238886' 
to_wa = 'whatsapp:+917249836522' # उदा. whatsapp:+919876543210

url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

data = {
    'From': from_wa, 
    'To': to_wa, 
    'Body': '🚨 *CRITICAL ALERT: CROWD COMMAND CENTER*\n\nCapacity breach or Panic detected in Sector A. Please dispatch Quick Response Team immediately!'
}

print("Sending message...")
response = requests.post(url, data=data, auth=HTTPBasicAuth(account_sid, auth_token))

# हे तुला सांगेल की नक्की काय चुकतंय!
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")