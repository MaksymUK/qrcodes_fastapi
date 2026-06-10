from os import getenv

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime


async def send_scan_notification(
        company_name: str,
        job_title: str
):
    message = Mail(
        from_email=getenv("FROM_EMAIL"),
        to_emails=getenv("ADMIN_EMAIL"),
        subject="QR Code Scan Alert",
        html_content=f"""
            <h2>QR Code Scan Alert</h2>

            <p><strong>Company:</strong> {company_name}</p>
            <p><strong>Job Title:</strong> {job_title}</p>
            <p><strong>Time scanned:</strong> {datetime.now()}</p>
            """
    )
    sg = SendGridAPIClient(
        getenv("SENDGRID_API_KEY")
    )

    sg.send(message)

