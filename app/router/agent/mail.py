from fastapi import APIRouter
from chains.company.models import UserInfo
from pydantic import BaseModel
from chains.mail.calendar_message.agent import CalendarMessageAgent
from modules.config import model
from features.calendar.services.common_calendar_service import CandidateDay
from typing import List

mail_agent_router = APIRouter()

@mail_agent_router.post("/")
async def mail_agent():
    pass



class MailDocumentCalendarRequest(BaseModel):
    candidate_days: List[CandidateDay]

# 候補日提案用の
@mail_agent_router.post("/create/calendar")
async def create_mail_document_calendar(request: MailDocumentCalendarRequest):
    print("request",request)
    agent = CalendarMessageAgent(llm=model)
    chain = agent.get_chain()
    result = await chain.ainvoke(request.candidate_days)
    return result