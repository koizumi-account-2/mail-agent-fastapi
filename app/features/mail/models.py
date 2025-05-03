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

class MailAnalysisResult(BaseModel):
    tasks: list[Task] = Field(default_factory=list, description="残タスク一覧")
    summary: str = Field(...,description="メールのまとめ")