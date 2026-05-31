import os
import uuid

import pandas as pd
import qrcode
from os import getenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime

from db.engine import SessionLocal
from db.models import DBRecipients, DBScanEvents

BASE_URL = getenv("BASE_URL", "http://localhost:8000")
QR_FOLDER = "qr_codes"

os.makedirs(QR_FOLDER, exist_ok=True)

app = FastAPI()

app.mount(
    "/qr_codes",
    StaticFiles(directory=QR_FOLDER),
    name="qr_codes"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

################### Excel → QR generation ############################

@app.post("/upload-recipients")
async def upload_recipients(file: UploadFile = File(...)):
    temp_file = f"temp_{file.filename}"

    try:
        # Save uploaded Excel file
        with open(temp_file, "wb") as f:
            f.write(await file.read())

        # Read Excel
        df = pd.read_excel(temp_file)

        # Normalize column names
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
        )

        # Validate required columns
        required_columns = ["name", "surname", "company_name"]

        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing columns: {', '.join(missing_columns)}"
            )

        db = SessionLocal()

        qr_image_urls = []
        tracking_urls = []

        try:
            for _, row in df.iterrows():

                # Skip empty rows
                if pd.isna(row["name"]):
                    continue

                token = str(uuid.uuid4())

                # URL encoded inside QR code
                tracking_url = f"{BASE_URL}/scan/{token}"

                # Physical file path
                qr_filename = f"{token}.png"
                qr_file_path = os.path.join(QR_FOLDER, qr_filename)

                # Public URL for Word Mail Merge
                qr_public_url = (
                    f"{BASE_URL}/qr_codes/{qr_filename}"
                )

                # Generate QR image
                qr = qrcode.make(tracking_url)
                qr.save(qr_file_path)

                recipient = DBRecipients(
                    name=str(row["name"]).strip(),
                    surname=str(row["surname"]).strip()
                    if pd.notna(row["surname"]) else None,
                    company_name=str(row["company_name"]).strip()
                    if pd.notna(row["company_name"]) else None,
                    qr_token=token,
                    qr_image_url=qr_public_url,
                )

                db.add(recipient)

                qr_image_urls.append(qr_public_url)
                tracking_urls.append(tracking_url)

            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

        # Add columns for Word Mail Merge
        df["qr_code_image"] = qr_image_urls
        df["tracking_url"] = tracking_urls

        output_excel = "recipients_with_qr.xlsx"
        df.to_excel(output_excel, index=False)

        return FileResponse(
            path=output_excel,
            filename=output_excel,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

#################### QR scan → Tracking #####################

from fastapi import Request
from fastapi.responses import RedirectResponse

@app.get("/scan/{token}")
async def scan_qr(token: str, request: Request):

    db = SessionLocal()

    recipient = (
        db.query(DBRecipients)
        .filter(DBRecipients.qr_token == token)
        .first()
    )

    if not recipient:
        raise HTTPException(status_code=404, detail="Invalid QR code")

    recipient.total_scans += 1
    recipient.last_scanned_at = datetime.now()

    if recipient.first_scanned_at is None:
        recipient.first_scanned_at = recipient.last_scanned_at

    db.commit()
    db.close()

    return RedirectResponse(
        url="YOUR_GOOGLE_DRIVE_PDF_LINK"
    )
