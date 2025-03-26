from config import SENDER_ADDR, SENDER_PASS, RECEIVER_ADDRS

from email.mime.text import MIMEText
import smtplib


def send_emails(pisciner, project):
    msg = MIMEText(
        f"""<html> <body><img src="{pisciner['image']['link']}" width="300" height="225"><br><small>{pisciner['login']} ({pisciner['usual_full_name']})</small><p><b>{pisciner['login']}</b>, <b>{project['project']['slug']}</b> projesini <b>{pisciner['location']}</b> lokasyonunda gönderdi.</p></body></html>""",
        "html",
    )
    msg["Subject"] = "proje veren var tutorum"
    msg["From"] = f"emirhan <{SENDER_ADDR}>"
    msg["To"] = ", ".join(RECEIVER_ADDRS)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(SENDER_ADDR, SENDER_PASS)
        smtp_server.sendmail(SENDER_ADDR, RECEIVER_ADDRS, msg.as_string())
