from fastapi import APIRouter, Header, HTTPException, Depends
from features.mail.services.imp.gmail_service import GmailService
from util.common import get_access_token

mail_router = APIRouter()

@mail_router.post("/test")
async def get_mail_thread_ids(access_token: str = Depends(get_access_token)):

    gmail_service = GmailService(access_token)
    mail = await gmail_service.get_gmail_thread_ids()
    mail_message = await gmail_service.get_mail_message_by_thread_id(mail["threadIds"][1])
    return mail_message


@mail_router.post("/threads")
async def get_mail_thread_ids(access_token: str = Depends(get_access_token)):
    gmail_service = GmailService(access_token)
    thread_ids = await gmail_service.get_gmail_thread_ids()
    return thread_ids


@mail_router.post("/threads/{thread_id}")
async def get_mail_message_by_thread_id(thread_id: str, access_token: str = Depends(get_access_token)):
    gmail_service = GmailService(access_token)
    mail_message = await gmail_service.get_mail_message_by_thread_id(thread_id)
    return mail_message


@mail_router.post("/messages/{message_id}")
async def get_gmail_message_by_id(message_id: str, access_token: str = Depends(get_access_token)):
    gmail_service = GmailService(access_token)
    mail_message = await gmail_service.get_gmail_message_by_id(message_id)
    return mail_message

