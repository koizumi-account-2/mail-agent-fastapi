from fastapi import APIRouter, Header, HTTPException, Depends
from features.mail.services.imp.gmail_service import GmailService
from util.common import get_access_token
from features.mail.schemas.mail_schema import ThreadListResponse
from features.mail.agent import MailAnalysisAgent
from features.mail.models import MailMessage
from modules.config import model
from fastapi import Request
mail_router = APIRouter()

@mail_router.post("/test")
async def get_mail_thread_ids(access_token: str = Depends(get_access_token)):

    gmail_service = GmailService(access_token)
    mail = await gmail_service.get_gmail_thread_ids()
    mail_message = await gmail_service.get_mail_message_by_thread_id(mail["threadIds"][1])
    return mail_message

@mail_router.post("/analyze/{thread_id}")
async def mail_analyze(thread_id: str, request: Request,access_token: str = Depends(get_access_token)):
    body = await request.json()
    gmail_service = GmailService(access_token)
    response = await gmail_service.get_mail_message_by_thread_id(thread_id)
    print("email_messages",len(response.messages))
    print("last",response.messages[0].id)
    current_situation = body["current_situation"]
    print("current_situation",current_situation)
    my_info = body["my_info"]
    latest_message_id = current_situation["latest_message_id"]
    existing_tasks = current_situation["existing_tasks"]
    my_info = "A株式会社 営業部 A"
    agent = MailAnalysisAgent(llm = model)
    result = agent.run(email_messages=response.messages, my_info=my_info, latest_message_id=latest_message_id, existing_tasks=existing_tasks, current_situation=current_situation)
    result.latest_message_id = response.messages[0].id
    return result

@mail_router.get("/threads")
async def get_mail_thread_ids(access_token: str = Depends(get_access_token)):
    gmail_service = GmailService(access_token)
    thread_ids: ThreadListResponse = await gmail_service.get_gmail_thread_ids()
    return thread_ids


@mail_router.get("/threads/{thread_id}")
async def get_mail_message_by_thread_id(thread_id: str, access_token: str = Depends(get_access_token)):
    gmail_service = GmailService(access_token)
    mail_message = await gmail_service.get_mail_message_by_thread_id(thread_id)
    return mail_message


@mail_router.get("/messages/{message_id}")
async def get_gmail_message_by_id(message_id: str, access_token: str = Depends(get_access_token)):
    gmail_service = GmailService(access_token)
    mail_message = await gmail_service.get_gmail_message_by_id(message_id)
    return mail_message

