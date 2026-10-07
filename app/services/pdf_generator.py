import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generate_pdf_certificate(recipient_name: str, course_name: str, issue_date: str, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    c = canvas.Canvas(output_path, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Border
    c.setLineWidth(5)
    c.setStrokeColor(colors.HexColor("#1A365D"))
    c.rect(20, 20, width - 40, height - 40)
    
    c.setLineWidth(2)
    c.setStrokeColor(colors.HexColor("#D69E2E"))
    c.rect(28, 28, width - 56, height - 56)

    # Text Content
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(colors.HexColor("#1A365D"))
    c.drawCentredString(width / 2, height - 120, "CERTIFICATE OF COMPLETION")

    c.setFont("Helvetica", 16)
    c.setFillColor(colors.HexColor("#4A5568"))
    c.drawCentredString(width / 2, height - 180, "This is proudly presented to")

    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(colors.HexColor("#2B6CB0"))
    c.drawCentredString(width / 2, height - 240, recipient_name)

    c.setFont("Helvetica", 16)
    c.setFillColor(colors.HexColor("#4A5568"))
    c.drawCentredString(width / 2, height - 290, "for successfully completing the course")

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor("#2D3748"))
    c.drawCentredString(width / 2, height - 340, course_name)

    c.setFont("Helvetica", 12)
    c.drawString(60, 60, f"Date: {issue_date}")
    
    c.save()
    return output_path