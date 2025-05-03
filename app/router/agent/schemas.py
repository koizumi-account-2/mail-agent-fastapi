from pydantic import BaseModel
from chains.company.models import UserInfo

class CompanyInfoFullRequest(BaseModel):
    company_name: str
    user_info: UserInfo