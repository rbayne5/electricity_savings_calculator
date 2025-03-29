from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

def create_test_tariff():
    """Create a test tariff PDF with sample data."""
    c = canvas.Canvas("tests/test_data/tariff.pdf", pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 1*inch, "Sample Electric Utility Tariff")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 1.5*inch, "Rate Schedule: Commercial & Industrial Storage")
    c.drawString(1*inch, height - 2*inch, "Effective Date: January 1, 2024")

    # Time-of-Use Periods
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 3*inch, "Time-of-Use Periods")
    
    tou_data = [
        ['Period', 'Hours', 'Days'],
        ['Peak', '4:00 PM - 9:00 PM', 'Weekdays'],
        ['Partial-Peak', '7:00 AM - 4:00 PM', 'Weekdays'],
        ['Off-Peak', '9:00 PM - 7:00 AM', 'All Days'],
        ['Super Off-Peak', '12:00 AM - 6:00 AM', 'Weekends']
    ]
    
    table = Table(tou_data, colWidths=[2*inch, 2.5*inch, 2*inch])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 10),
        ('TOPPADDING', (0,1), (-1,-1), 12)
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 1*inch, height - 5*inch)

    # Energy Charges
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 6*inch, "Energy Charges (per kWh)")
    
    rate_data = [
        ['Period', 'Summer (Jun-Sep)', 'Winter (Oct-May)'],
        ['Peak', '$0.35424', '$0.28339'],
        ['Partial-Peak', '$0.25339', '$0.22254'],
        ['Off-Peak', '$0.18254', '$0.15169'],
        ['Super Off-Peak', '$0.12169', '$0.10085']
    ]
    
    table2 = Table(rate_data, colWidths=[2*inch, 2.5*inch, 2*inch])
    table2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 10),
        ('TOPPADDING', (0,1), (-1,-1), 12)
    ]))
    table2.wrapOn(c, width, height)
    table2.drawOn(c, 1*inch, height - 8*inch)

    # Additional Conditions
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 9*inch, "Additional Conditions")
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, height - 9.5*inch, "1. Minimum charge: $10.00 per day")
    c.drawString(1*inch, height - 9.8*inch, "2. Power factor adjustment: Applied when power factor < 95%")
    c.drawString(1*inch, height - 10.1*inch, "3. Holidays are considered off-peak periods")

    c.save()

if __name__ == "__main__":
    create_test_tariff() 