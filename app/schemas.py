from pydantic import BaseModel


class RecipientsBase(BaseModel):
    name: str
    surname: str
    company_name: str
    destination_url: str


class RecipientsCreate(RecipientsBase):
    pass