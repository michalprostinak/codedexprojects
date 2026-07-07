"""
Generovanie PDF prepúšťacej správy (discharge report).
"""
import os
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

OUTPUT_DIR = "discharge_reports"


def generate_discharge_report(patient):
    """
    Vytvorí PDF prepúšťaciu správu pre daného pacienta.
    Vráti cestu k vytvorenému súboru.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filename = f"discharge_{patient.id}_{patient.name.replace(' ', '_')}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "HospitalTitle",
        parent=styles["Title"],
        fontSize=20,
        spaceAfter=2,
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Heading2"],
        alignment=1,  # center
        spaceAfter=20,
    )
    label_style = ParagraphStyle(
        "Label",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=colors.HexColor("#444444"),
    )
    value_style = ParagraphStyle(
        "Value",
        parent=styles["Normal"],
        fontSize=12,
        spaceAfter=12,
    )

    story = []

    story.append(Paragraph("CITY HOSPITAL", title_style))
    story.append(Paragraph("DISCHARGE REPORT", subtitle_style))

    # Tabuľka so základnými údajmi
    data = [
        ["Patient:", patient.name],
        ["Age:", str(patient.age)],
        ["Department:", patient.department or "-"],
        ["Diagnosis:", patient.diagnosis],
        ["Treatment:", patient.treatment],
        ["Status:", patient.status],
        ["Date of discharge:", date.today().strftime("%d.%m.%Y")],
    ]

    table = Table(data, colWidths=[5 * cm, 10 * cm])
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#cccccc")),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 20))

    story.append(Paragraph("Doctor's notes:", label_style))
    story.append(Paragraph(patient.notes or "-", value_style))

    story.append(Spacer(1, 30))
    story.append(Paragraph("Responsible doctor:", label_style))
    story.append(Paragraph(f"Dr. {patient.doctor_name}", value_style))

    story.append(Spacer(1, 40))
    story.append(Paragraph("Doctor signature: ____________________", styles["Normal"]))

    doc.build(story)
    return filepath
