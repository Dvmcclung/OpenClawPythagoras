#!/usr/bin/env python3
"""Generate PDF of the Elegant Solutions white paper using reportlab."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import re

OUTPUT = "/home/dale/.openclaw/pythagoras-workspace/papers/elegant_solutions_whitepaper.pdf"
MD_FILE = "/home/dale/.openclaw/pythagoras-workspace/papers/elegant_solutions_whitepaper.md"

with open(MD_FILE, "r") as f:
    lines = f.readlines()

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    rightMargin=1.1*inch,
    leftMargin=1.1*inch,
    topMargin=1.1*inch,
    bottomMargin=1.1*inch,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title",
    fontSize=22,
    leading=28,
    textColor=colors.HexColor("#1a1a2e"),
    spaceAfter=6,
    alignment=TA_CENTER,
    fontName="Times-Bold",
)
subtitle_style = ParagraphStyle(
    "Subtitle",
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#444444"),
    spaceAfter=4,
    alignment=TA_CENTER,
    fontName="Times-Italic",
)
h1_style = ParagraphStyle(
    "H1",
    fontSize=15,
    leading=20,
    textColor=colors.HexColor("#1a1a2e"),
    spaceBefore=18,
    spaceAfter=6,
    fontName="Times-Bold",
)
h2_style = ParagraphStyle(
    "H2",
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#2c3e50"),
    spaceBefore=12,
    spaceAfter=4,
    fontName="Times-Bold",
)
h3_style = ParagraphStyle(
    "H3",
    fontSize=11,
    leading=15,
    textColor=colors.HexColor("#34495e"),
    spaceBefore=10,
    spaceAfter=3,
    fontName="Times-BoldItalic",
)
body_style = ParagraphStyle(
    "Body",
    fontSize=11,
    leading=16,
    textColor=colors.HexColor("#1a1a1a"),
    spaceAfter=8,
    alignment=TA_JUSTIFY,
    fontName="Times-Roman",
)
bullet_style = ParagraphStyle(
    "Bullet",
    fontSize=11,
    leading=15,
    textColor=colors.HexColor("#1a1a1a"),
    spaceAfter=4,
    leftIndent=20,
    fontName="Times-Roman",
)
italic_body = ParagraphStyle(
    "ItalicBody",
    fontSize=11,
    leading=16,
    textColor=colors.HexColor("#2c3e50"),
    spaceAfter=8,
    alignment=TA_JUSTIFY,
    leftIndent=30,
    rightIndent=30,
    fontName="Times-Italic",
)
footer_style = ParagraphStyle(
    "Footer",
    fontSize=9,
    leading=12,
    textColor=colors.HexColor("#888888"),
    alignment=TA_CENTER,
    fontName="Times-Italic",
)

def escape_xml(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text

def process_inline(text):
    """Convert markdown inline formatting to reportlab XML."""
    text = escape_xml(text)
    # Bold italic ***text***
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Bold **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic *text*
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # Italic _text_
    text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)
    # Code `text`
    text = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', text)
    return text

story = []
i = 0

while i < len(lines):
    line = lines[i].rstrip()

    # Title (first # line)
    if line.startswith("# ") and i < 5:
        story.append(Paragraph(process_inline(line[2:]), title_style))
        i += 1
        continue

    # Byline / subtitle (italic lines near top)
    if line.startswith("**A White Paper") or line.startswith("*Commissioned"):
        story.append(Paragraph(process_inline(line.strip("*")), subtitle_style))
        i += 1
        continue

    # HR
    if line.startswith("---"):
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
        story.append(Spacer(1, 6))
        i += 1
        continue

    # H2 ##
    if re.match(r'^## \d+\.', line) or (line.startswith("## ") and not line.startswith("### ")):
        story.append(Paragraph(process_inline(line[3:]), h1_style))
        i += 1
        continue

    # H3 ###
    if line.startswith("### "):
        story.append(Paragraph(process_inline(line[4:]), h2_style))
        i += 1
        continue

    # H4 ####
    if line.startswith("#### "):
        story.append(Paragraph(process_inline(line[5:]), h3_style))
        i += 1
        continue

    # Bullet
    if line.startswith("- "):
        story.append(Paragraph("• " + process_inline(line[2:]), bullet_style))
        i += 1
        continue

    # Block quote / hypothesis (indented italic)
    if line.startswith("> "):
        story.append(Paragraph(process_inline(line[2:]), italic_body))
        i += 1
        continue

    # Italic block (hypothesis)
    if line.startswith("*") and line.endswith("*") and len(line) > 2 and not line.startswith("**"):
        story.append(Paragraph(process_inline(line), italic_body))
        i += 1
        continue

    # Empty line
    if not line.strip():
        story.append(Spacer(1, 4))
        i += 1
        continue

    # Regular paragraph
    if line.strip():
        story.append(Paragraph(process_inline(line), body_style))

    i += 1

# Footer
story.append(Spacer(1, 24))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
story.append(Spacer(1, 6))
story.append(Paragraph("Pythagoras (𝚷) · March 2026 · Commissioned by Dale McClung", footer_style))

doc.build(story)
print(f"PDF written to {OUTPUT}")
