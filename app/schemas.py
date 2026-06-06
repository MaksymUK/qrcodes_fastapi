from pydantic import BaseModel


class RecipientsBase(BaseModel):
    first_name: str
    last_name: str
    job_title: str
    company_name: str
    destination_url: str

class ScanEventsBase(BaseModel):
    ip_address: str
    country: str
    city: str


class RecipientsCreate(RecipientsBase):
    pass