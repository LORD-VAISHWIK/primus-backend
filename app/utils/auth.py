import os
import smtplib
from email.mime.text import MIMEText
import ssl
import time

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER or "no-reply@example.com")
SMTP_TLS = os.getenv("SMTP_TLS", "1") not in ("0", "false", "False")
SMTP_SSL = os.getenv("SMTP_SSL", "0") not in ("0", "false", "False")
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8000")

def send_email(to_email: str, subject: str, html_body: str) -> None:
    msg = MIMEText(html_body, "html")
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = to_email

    # Try configured SMTP first (kept for legacy email flows; not used with Firebase-only login)
    if SMTP_HOST:
        try:
            # Implicit SSL (e.g., port 465) or explicit SMTP_SSL requested
            if SMTP_SSL or str(SMTP_PORT) == "465":
                with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ssl.create_default_context()) as server:
                    if SMTP_USER and SMTP_PASS:
                        server.login(SMTP_USER, SMTP_PASS)
                    server.sendmail(SMTP_FROM, [to_email], msg.as_string())
                    return
            else:
                with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                    server.ehlo()
                    if SMTP_TLS:
                        try:
                            context = ssl.create_default_context()
                            server.starttls(context=context)
                        except Exception:
                            pass
                    if SMTP_USER and SMTP_PASS:
                        server.login(SMTP_USER, SMTP_PASS)
                    server.sendmail(SMTP_FROM, [to_email], msg.as_string())
                    return
        except Exception as e:
            print(f"[SMTP ERROR] Primary SMTP failed: {e}. Falling back to localhost:1025")

    # Fallback: local dev SMTP (e.g., smtp4dev/MailHog) without auth/TLS
    try:
        with smtplib.SMTP("127.0.0.1", 1025, timeout=5) as server:
            server.sendmail(SMTP_FROM, [to_email], msg.as_string())
            return
    except Exception as e:
        # Final fallback: print to console and also write to a dev inbox file for quick access
        print(f"[DEV EMAIL] (no SMTP available) To: {to_email} | Subject: {subject}\n{html_body}")
        try:
            inbox_dir = os.getenv("DEV_INBOX_DIR", "./dev_emails")
            os.makedirs(inbox_dir, exist_ok=True)
            ts = int(time.time())
            safe_to = to_email.replace('@','_').replace(':','_')
            path = os.path.join(inbox_dir, f"{ts}_{safe_to}.html")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html_body)
        except Exception:
            pass

def build_email_verification_link(token: str) -> str:
    return f"{APP_BASE_URL}/api/auth/verify-email?token={token}"
