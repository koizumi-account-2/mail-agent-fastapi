from pydantic import BaseModel, Field
from typing import List


class CompanyInfoAnalysisResult(BaseModel):
    company_name: str = Field(..., description="対象となった企業名")
    location: str = Field(..., description="対象となった企業の所在地")
    industry: str = Field(..., description="対象となった企業の業界")
    business_content: str = Field(..., description="対象となった企業の事業内容")
    employee_number: int = Field(..., description="対象となった企業の従業員数")