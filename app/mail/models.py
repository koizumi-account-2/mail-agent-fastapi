from pydantic import BaseModel, Field


class MailAnalysisResult(BaseModel):
    email_text: str = Field(...,description="メールの本文")   
    tasks: list[str] = Field(default_factory=list, description="残タスク一覧")
    summary: str = Field(...,description="メールのまとめ")