"""
AI Video Market Watch — Email Sender

Günlük HTML raporu Gmail üzerinden gönderir.
HTML rapor doğrudan mail gövdesine embed edilir.

Kullanım:
    from email_sender import send_daily_report_email
    send_daily_report_email(html_path, date="2026-02-26")
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path

from config import EMAIL_SENDER, EMAIL_RECIPIENT, GMAIL_APP_PASSWORD, REPORTS_DIR


def send_daily_report_email(html_path, date=None):
    """
    Günlük HTML raporu email olarak gönderir.

    Args:
        html_path: Path — HTML rapor dosya yolu
        date: str — rapor tarihi (konu satırında kullanılır)

    Returns:
        bool: başarılı ise True
    """
    if not GMAIL_APP_PASSWORD:
        print("  [EMAIL] GMAIL_APP_PASSWORD .env'de tanımlı değil, mail atlanıyor.")
        return False

    html_path = Path(html_path)
    if not html_path.exists():
        print(f"  [EMAIL] HTML dosya bulunamadı: {html_path}")
        return False

    # HTML içeriğini oku
    html_content = html_path.read_text(encoding="utf-8")

    # Logo varsa CID ile embed et (inline image)
    logo_path = html_path.parent / "Untitled 2.jpg"
    if logo_path.exists():
        html_content = html_content.replace(
            'src="Untitled 2.jpg"',
            'src="cid:vmw_logo"'
        )

    # Email oluştur
    msg = MIMEMultipart("related")
    msg["Subject"] = f"VMW Günlük Rapor — {date or 'Bugün'}"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT

    # HTML gövdesi
    html_part = MIMEText(html_content, "html", "utf-8")
    msg.attach(html_part)

    # Logo embed (CID)
    if logo_path.exists():
        with open(logo_path, "rb") as img_file:
            logo_img = MIMEImage(img_file.read(), _subtype="jpeg")
            logo_img.add_header("Content-ID", "<vmw_logo>")
            logo_img.add_header("Content-Disposition", "inline", filename="logo.jpg")
            msg.attach(logo_img)

    # Gönder
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, GMAIL_APP_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        print(f"  [EMAIL] Rapor gönderildi → {EMAIL_RECIPIENT}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("  [EMAIL] Gmail kimlik doğrulama hatası. App Password'ü kontrol edin.")
        return False
    except Exception as e:
        print(f"  [EMAIL] Gönderim hatası: {e}")
        return False
