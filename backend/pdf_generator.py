from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(summary, transcript):

    filename = "Meeting_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "AI Meeting Intelligence Report",
        styles["Title"]
    )

    content.append(title)

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "<b>Meeting Summary</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            summary.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            "<b>Transcript</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            transcript.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(content)

    return filename