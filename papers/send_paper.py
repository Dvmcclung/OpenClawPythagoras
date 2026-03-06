#!/usr/bin/env python3
import smtplib, os, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

SMTP_USER = os.environ.get("ICLOUD_SMTP_USER")
SMTP_PASS = os.environ.get("ICLOUD_SMTP_PASS")
SMTP_HOST = "smtp.mail.me.com"
SMTP_PORT = 587

if not SMTP_USER or not SMTP_PASS:
    print("ERROR: ICLOUD_SMTP_USER or ICLOUD_SMTP_PASS not set")
    sys.exit(1)

TO = "dvmcclung@me.com"
SUBJECT = "The Elegant Solution — A White Paper by Pythagoras"
PDF_PATH = "/home/dale/.openclaw/pythagoras-workspace/papers/elegant_solutions_whitepaper.pdf"

body = """Dale,

Attached is the white paper you commissioned this morning: The Elegant Solution — Is There Measurable Value in Mathematical Elegance?

The paper covers the historical definition of elegance from Euler through Kolmogorov complexity theory, examines your conjecture about the art-music-mathematics connection (and proposes a mechanistic version of it), formulates three independently testable hypotheses, and designs a concrete experiment using supply chain demand forecasting as the testbed.

It runs approximately 3,500 words.

— Pythagoras (𝚷)
"""

msg = MIMEMultipart()
msg["From"] = SMTP_USER
msg["To"] = TO
msg["Subject"] = SUBJECT
msg.attach(MIMEText(body, "plain"))

with open(PDF_PATH, "rb") as f:
    pdf_data = f.read()

attachment = MIMEApplication(pdf_data, _subtype="pdf")
attachment.add_header("Content-Disposition", "attachment", filename="elegant_solutions_whitepaper.pdf")
msg.attach(attachment)

with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
    server.ehlo()
    server.starttls()
    server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(SMTP_USER, [TO], msg.as_string())

print("Email sent successfully.")
