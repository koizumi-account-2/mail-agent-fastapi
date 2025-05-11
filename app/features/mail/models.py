from pydantic import BaseModel, Field

class MailMessage(BaseModel):
    sender: str
    content: str
    date: str
    subject: str
    id: str

class Task(BaseModel):
    task_name: str = Field(...,description="タスク名")
    assigned_to: str = Field(...,description="タスクの担当者")

class CompanyLocation(BaseModel):
    company_name: str = Field(...,description="会社名")
    company_address: str = Field(...,description="会社住所")

class MailAnalysisResult(BaseModel):
    tasks: list[Task] = Field(default_factory=list, description="残タスク一覧")
    summary: str = Field(...,description="メールのまとめ")
    latest_message_id: str = Field(...,description="最新のメールのID")
    company_location: CompanyLocation = Field(...,description="会社住所")