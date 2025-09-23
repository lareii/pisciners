from config import (
    SENDER_ADDR,
    SENDER_PASS,
    RECEIVER_ADDRS,
    SMTP_SERVER,
    SMTP_PORT
)

from email.mime.text import MIMEText
import smtplib


def send_emails(pisciner, project_slug):
    msg = MIMEText(
        f"""<html> <body><img src="{pisciner['image']['link']}" width="300" height="225"><br><small>{pisciner['login']} ({pisciner['usual_full_name']})</small><p><b>{pisciner['login']}</b>, <b>{project_slug}</b> projesini <b>{pisciner['location']}</b> lokasyonunda gönderdi.</p></body></html>""",
        "html",
    )
    msg["Subject"] = f"{pisciner['login']}, {project_slug} projesini gönderdi!"
    msg["From"] = f"pisciners-bot <{SENDER_ADDR}>"
    msg["To"] = ", ".join(RECEIVER_ADDRS)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp_server:
        smtp_server.login(SENDER_ADDR, SENDER_PASS)
        smtp_server.sendmail(SENDER_ADDR, RECEIVER_ADDRS, msg.as_string())
