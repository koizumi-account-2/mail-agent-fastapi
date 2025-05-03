from pydantic import BaseModel, Field
from typing import List

class NewsArticle(BaseModel):
    title: str = Field(..., description="ニュース記事のタイトル")
    summary: str = Field(..., description="記事の要約")
    url: str = Field(..., description="記事のURL")

class CompanyNewsAnalysisResult(BaseModel):
    company_name: str = Field(..., description="対象となった企業名")
    positive_news: List[NewsArticle] = Field(..., description="ポジティブなニュース一覧")
    negative_news: List[NewsArticle] = Field(..., description="ネガティブなニュース一覧")