from abc import ABC, abstractmethod
from typing import List, Dict
from mail.schemas.mail_schema import ThreadListResponse, MailMessageDTO
class EmailService(ABC):

    @abstractmethod
    async def get_gmail_thread_ids(self, max_results: int = 10) -> List[ThreadListResponse]:
        ...

    @abstractmethod
    async def get_mail_message_by_thread_id(self, thread_id: str) -> List[MailMessageDTO]:
        ...

    @abstractmethod
    async def get_gmail_message_by_id(self, message_id: str) -> str:
        ...