import os
from fpdf import FPDF
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

# लोड API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_ai_insights(peak_crowd, total_alerts):
    """
    Gemini AI ला गर्दीचा डेटा पाठवून पोलिसांसाठी सल्ले (Recommendations) मागवणे.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Act as an expert crowd control analyst for the local police department. 
        A recent event had a peak crowd of {peak_crowd} people and triggered {total_alerts} high-risk proximity alerts. 
        Write a short, professional 3-point recommendation for the police to improve safety and avoid stampedes for the next event. 
        Keep it concise and actionable.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "AI Analysis unavailable. Recommendation: Increase physical barricades, deploy more personnel at entry points, and monitor CCTV feeds actively."

def create_safety_report(max_crowd, alerts_triggered):
    """
    AI चे सल्ले घेऊन एक प्रोफेशनल PDF फाईल तयार करणे.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    date_str = datetime.now().strftime("%B %d, %Y")
    
    # 🧠 AI कडून पोलिसांसाठी रिपोर्ट लिहून घेणे
    ai_insights = generate_ai_insights(max_crowd, alerts_triggered)
    
    # PDF डिझाईन सुरू
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Header (Title)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(220, 50, 50) # लाल रंग
    pdf.cell(200, 10, txt="SMART CROWD SURVEILLANCE - INCIDENT REPORT", ln=True, align='C')
    pdf.set_text_color(0, 0, 0) # काळा रंग
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Date: {date_str} | Location: Main Gate (Cam 1)", ln=True, align='C')
    pdf.ln(10)
    
    # गर्दीची आकडेवारी
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="1. Crowd Statistics:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"- Peak Crowd Count: {max_crowd} persons detected at once.", ln=True)
    pdf.cell(200, 10, txt=f"- High-Risk Alerts Triggered: {alerts_triggered} times.", ln=True)
    pdf.ln(10)
    
    # AI Analysis Section
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 100, 200) # निळा रंग
    pdf.cell(200, 10, txt="2. AI Predictive Analysis & Police Recommendations:", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=11)
    
    # Gemini च्या टेक्स्ट मधले Markdown (* आणि **) काढून टाकणे जेणेकरून PDF मध्ये नीट दिसेल
    clean_text = ai_insights.replace('**', '').replace('*', '-')
    pdf.multi_cell(0, 10, txt=clean_text)
    
    # Footer
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="Generated automatically by SVERI AI Crowd Intelligence System", ln=True, align='C')
    
    # PDF सेव्ह करा
    filename = f"Incident_Report_{timestamp}.pdf"
    pdf.output(filename)
    return filename