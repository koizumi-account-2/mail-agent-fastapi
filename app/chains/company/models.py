from pydantic import BaseModel, Field
from typing import List, Optional
from util.common import UserInfo


class NewsArticle(BaseModel):
    title: str = Field(..., description="ニュース記事のタイトル")
    summary: str = Field(..., description="記事の要約")
    url: str = Field(..., description="記事のURL")

class CompanyNewsAnalysisResult(BaseModel):
    company_name: str = Field(..., description="対象となった企業名")
    positive_news: List[NewsArticle] = Field(..., description="ポジティブなニュース一覧")
    negative_news: List[NewsArticle] = Field(..., description="ネガティブなニュース一覧")

class CompanyInfoAnalysisResult(BaseModel):
    company_name: str = Field(..., description="対象となった企業名")
    location: str = Field(..., description="対象となった企業の所在地")
    industry: str = Field(..., description="対象となった企業の業界")
    business_content: str = Field(..., description="対象となった企業の事業内容")
    employee_number: int = Field(..., description="対象となった企業の従業員数")

class TravelTimeResult(BaseModel):
    start_address: str = Field(..., description="出発地点")
    end_address: str = Field(..., description="目的地")
    travel_time: int = Field(..., description="対象となった企業からユーザーの所在地までの所要時間")
    distance_text: str = Field(..., description="対象となった企業からユーザーの所在地までの距離")
    duration_text: str = Field(..., description="対象となった企業からユーザーの所在地までの所要時間")
    duration_seconds: int = Field(..., description="対象となった企業からユーザーの所在地までの所要時間(秒)")

class CompanyInfoFullResult(BaseModel):
    company_info: CompanyInfoAnalysisResult = Field(..., description="企業の基本情報")
    company_news: CompanyNewsAnalysisResult = Field(..., description="企業のニュース情報")
    travel_time: TravelTimeResult = Field(..., description="対象となった企業からユーザーの所在地までの所要時間")
