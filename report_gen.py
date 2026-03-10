def create_safety_report(peak_count, alert_count):
    """Generates a summary of the surveillance session."""
    filename = "Safety_Audit_Report.txt" # आपण सध्या साध्या टेक्स्ट फाईलमध्ये सेव्ह करूया
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== SMART CROWD INTELLIGENCE SYSTEM AUDIT ===\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Peak Crowd Observed: {peak_count} persons\n")
        f.write(f"Total Critical Alerts Issued: {alert_count}\n")
        f.write("Status: Session Concluded Successfully.\n")
        f.write("============================================\n")
    return filename