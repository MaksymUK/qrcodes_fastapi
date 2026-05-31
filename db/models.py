from datetime import datetime

from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, Identity
from sqlalchemy.orm import relationship

from db.engine import Base

class DBRecipients(Base):
    __tablename__ = "recipients"
    id = Column(BigInteger, Identity(always=False), primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String)
    company_name = Column(String)
    qr_token = Column(String, unique=True, nullable=False)
    destination_url = Column(String)
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

