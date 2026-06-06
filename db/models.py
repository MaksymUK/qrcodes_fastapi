from datetime import datetime

from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, Identity
from sqlalchemy.orm import relationship

from db.engine import Base

class DBRecipients(Base):
    __tablename__ = "recipients"
    id = Column(BigInteger, Identity(always=False), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    qr_token = Column(String, unique=True, nullable=False)
    destination_url = Column(String, nullable=False)
    qr_image_url = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    first_scanned_at = Column(DateTime)
    last_scanned_at = Column(DateTime)
    total_scans = Column(Integer, default=0)
    scans = relationship(
        "DBScanEvents",
        back_populates="recipient",
        cascade="all, delete-orphan"
    )


class DBScanEvents(Base):
    __tablename__ = "scan_events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipient_id = Column(ForeignKey("recipients.id"), nullable=False)
    scanned_at = Column(DateTime, default=datetime.now)
    ip_address = Column(String)
    country = Column(String)
    city = Column(String)
    recipient = relationship("DBRecipients", back_populates="scans")

