from fastapi import APIRouter, Header, HTTPException, Depends
from features.mail.services.imp.gmail_service import GmailService
from util.common import get_access_token
from features.mail.schemas.mail_schema import ThreadListResponse
from features.mail.agent import MailAnalysisAgent
from features.mail.models import MailMessage
from features.mail.schemas.mail_schema import MailMessageDTO
from modules.config import model
from fastapi import Request
mail_router = APIRouter()

@mail_router.get("/test")
async def get_mail_thread_ids(q:str = "no data"):
    test_mail_message =  [
        MailMessageDTO(
            id='AAAAAA', 
            snippet='', 
            subject='test data1', 
            sender='小泉舜敬', 
            date='Wed, 7 May 2025 17:41:41 +0900', 
            content='q:'+q
        ),
        MailMessageDTO(
            id='BBBBBB', 
            snippet='', 
            subject='test data2', 
            sender='小泉舜敬', 
            date='Wed, 7 May 2025 17:41:41 +0900', 
            content='q:'+q
        )
    ]
    return test_mail_message

@mail_router.post("/analyze/{thread_id}")
async def mail_analyze(thread_id: str, request: Request,access_token: str = Depends(get_access_token)):
    body = await request.json()
    gmail_service = GmailService(access_token)
    response = await gmail_service.get_mail_message_by_thread_id(thread_id)
    current_situation = body["current_situation"]
    my_info = body["my_info"]
    latest_message_id = current_situation["latest_message_id"]
    existing_tasks = current_situation["existing_tasks"]
    my_info = "エスコ・ジャパン株式会社 営業担当"
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

