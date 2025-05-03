from mail.services.email_service import EmailService
from google.oauth2.credentials import Credentials
from typing import List
from googleapiclient.discovery import build
from mail.schemas.mail_schema import ThreadListResponse, MailMessageDTO, ThreadDTO
from typing import Dict, Any
import base64, re
from modules.log import log_async

class GmailService(EmailService):
    def __init__(self, access_token: str):
        credentials = Credentials(
            token=access_token,
            scopes=["https://www.googleapis.com/auth/gmail.readonly"]
        )
        self.service = build("gmail", "v1", credentials=credentials) 

    @log_async
    async def get_gmail_thread_ids(self, max_results: int = 10,next_page_token: str = None) -> List[ThreadListResponse]:
        """
        GmailのthreadIdのリストを取得する
        """
        query_params = {
            "userId": "me",
            "maxResults": max_results,
        }
        if next_page_token:
            query_params["pageToken"] = next_page_token

        results = self.service.users().threads().list(**query_params).execute()
        threads = results.get("threads", [])
        next_page_token = results.get("nextPageToken")
        return {
            "threadIds": [t["id"] for t in threads],
            "nextPageToken": next_page_token
        }
    @log_async
    async def get_mail_message_by_thread_id(self, thread_id: str) -> ThreadDTO:
        """
        GmailのthreadIdからメールのリストを取得する
        """
        results = self.service.users().threads().get(userId="me", id=thread_id).execute()
        messages = results.get("messages", [])
        sorted_messages = sorted(messages, key=lambda msg: int(msg.get("internalDate", 0)))
        return ThreadDTO(
            threadId=thread_id,
            messages=[convert_message_to_dto(m) for m in sorted_messages]
        )
    
    @log_async
    async def get_gmail_message_by_id(self, message_id: str) -> str:
        """
        GmailのmessageIdから1通のメール本文を取得する
        """
        try:
            result = self.service.users().messages().get(userId="me", id=message_id).execute()
            payload = result.get("payload", {})
            return get_mail_body(payload)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch message {message_id}: {str(e)}")
        

# メールのヘッダーとボディを抽出する用の関数

def extract_header(headers: List[Dict[str, Any]], name: str) -> str:
    return next((h.get("value", "") for h in headers if h.get("name") == name), "")


def convert_message_to_dto(message: Dict[str, Any]) -> MailMessageDTO:
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    dto = MailMessageDTO(
        id=message.get("id", ""),
        snippet=message.get("snippet", ""),
        subject=extract_header(headers, "Subject"),
        sender=extract_header(headers, "From"),
        date=extract_header(headers, "Date"),
        content=get_mail_body(payload)
    )

    return dto



def decode_base64url(data: str) -> str:
    """Base64URLデコードしてUTF-8に変換"""
    padded = data + '=' * (-len(data) % 4)  # パディング調整
    return base64.urlsafe_b64decode(padded).decode('utf-8', errors='replace')

def remove_quoted_text(body: str) -> str:
    lines = body.splitlines()
    clean_lines = []

    quote_patterns = [
        re.compile(r"^On .+ wrote:$"),
        re.compile(r"^> .+"),
        re.compile(r"^From: .+"),
        re.compile(r"^-----Original Message-----$"),
        re.compile(r"^-+ Forwarded message -+$"),
        re.compile(r"^.+さんは書きました:$")
    ]

    for line in lines:
        if any(pat.match(line.strip()) for pat in quote_patterns):
            break
        clean_lines.append(line)

    return "\n".join(clean_lines)

def get_mail_body(payload: dict) -> str:
    if not payload:
        return ""

    # multipart: payload["parts"] がある場合
    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")
            body = part.get("body", {})
            if mime_type in ("text/plain", "text/html") and "data" in body:
                decoded = decode_base64url(body["data"])
                return remove_quoted_text(decoded)

    # 単一部構成: payload["body"]["data"] が直接ある
    if "body" in payload and "data" in payload["body"]:
        decoded = decode_base64url(payload["body"]["data"])
        return remove_quoted_text(decoded)

    return ""