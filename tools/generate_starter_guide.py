from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "hkgong-cantonese-starter-guide.pdf"


def build():
    registerFont(UnicodeCIDFont("STSong-Light"))

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="GuideTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=30,
            leading=33,
            textColor=colors.HexColor("#191513"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="GuideHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#a82924"),
            spaceBefore=18,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="GuideBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor("#3d352f"),
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Chinese",
            parent=styles["BodyText"],
            fontName="STSong-Light",
            fontSize=15,
            leading=20,
            textColor=colors.HexColor("#191513"),
        )
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        rightMargin=22 * mm,
        leftMargin=22 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title="HKGong Cantonese Starter Guide",
        author="HKGong",
    )

    story = [
        Paragraph("HKGong Cantonese Starter Guide", styles["GuideTitle"]),
        Paragraph(
            "A compact first guide for learners who want Cantonese to feel less scattered.",
            styles["GuideBody"],
        ),
        Spacer(1, 8),
        Paragraph("1. The Problem", styles["GuideHeading"]),
        Paragraph(
            "Cantonese learners often jump between separate tools: Jyutping charts, tone notes, "
            "dictionary apps, grammar explanations, character resources, listening clips, and practice games. "
            "That makes the language feel fragmented.",
            styles["GuideBody"],
        ),
        Paragraph(
            "HKGong is built around one simple idea: connect sounds, words, sentence structure, examples, "
            "characters, listening, writing, and practice in one learning system.",
            styles["GuideBody"],
        ),
        Paragraph("2. The First Study Path", styles["GuideHeading"]),
        Paragraph(
            "Start with sound, then words, then sentence structure. Do not begin by memorizing many random phrases.",
            styles["GuideBody"],
        ),
    ]

    path_rows = [
        ["Step", "Focus", "Why it matters"],
        ["1", "Sounds + Jyutping", "You need a way to hear and write the pronunciation."],
        ["2", "Core words", "Useful words become easier when sound and meaning connect."],
        ["3", "Sentence order", "Cantonese starts to make sense when you see the pattern."],
        ["4", "Examples", "Many examples make one structure feel natural."],
        ["5", "Practice", "Listening, writing, and games turn knowledge into memory."],
    ]
    table = Table(path_rows, colWidths=[18 * mm, 42 * mm, 94 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#191513")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("LEADING", (0, 0), (-1, -1), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#fff8ed")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#eadbc9")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.extend(
        [
            table,
            Paragraph("3. First Useful Sentence", styles["GuideHeading"]),
            Paragraph("你好，我想學廣東話。", styles["Chinese"]),
            Paragraph("nei5 hou2, ngo5 soeng2 hok6 gwong2 dung1 waa2.", styles["GuideBody"]),
            Paragraph("Hello, I want to learn Cantonese.", styles["GuideBody"]),
            Paragraph(
                "Notice the structure: greeting + I + want + learn + Cantonese. A good app should not only show "
                "the sentence. It should help you see the parts inside it.",
                styles["GuideBody"],
            ),
            Paragraph("4. Learner Languages", styles["GuideHeading"]),
            Paragraph(
                "HKGong is designed for many learners, including people who think in English, Catalan, French, "
                "Filipino, Indonesian, Malay, Spanish, German, and more.",
                styles["GuideBody"],
            ),
            Paragraph("5. What To Do Next", styles["GuideHeading"]),
            Paragraph(
                "Open HKGong and study one connected path: sounds, then words, then sentence building, then listening "
                "or writing practice. The goal is not to tap forever. The goal is to make Cantonese feel organized.",
                styles["GuideBody"],
            ),
            Spacer(1, 10),
            Paragraph("Download HKGong: https://hkgong.com", styles["GuideBody"]),
        ]
    )

    doc.build(story)


if __name__ == "__main__":
    build()
    print(f"Wrote {OUT}")
