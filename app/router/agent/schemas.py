from pydantic import BaseModel
from chains.company.models import UserInfo
from typing import Optional
class CompanyInfoFullRequest(BaseModel):
    company_name: str
    user_info: UserInfo
    company_address: Optional[str] = None