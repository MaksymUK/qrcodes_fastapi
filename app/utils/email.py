from os import getenv

from fastapi_mail import (FastMail, MessageSchema, ConnectionConfig)
from datetime import datetime

conf = ConnectionConfig(
    MAIL_USERNAME=getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=getenv("MAIL_PASSWORD"),
    MAIL_FROM=getenv("MAIL_FROM"),
    MAIL_SERVER=getenv("MAIL_SERVER"),
    MAIL_PORT=getenv("MAIL_PORT"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

async def send_scan_notification(
        company_name: str,
        job_title: str
):
    message = MessageSchema(
        subject="QR code scan alert",
        recipients=[getenv("ADMIN_EMAIL")],
        body=f"""
        {company_name} / {job_title} just scanned QR code
        Scan time: {datetime.now()}
        """,
        subtype="plain",
    )
    fm = FastMail(conf)
    await fm.send(message)
