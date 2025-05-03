from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from modules.config import model,tavily_retriever,ACCESS_TOKEN
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from chains.company.full_chain import CompanyInfoFullChain
from typing import Annotated
import asyncio

from features.mail.services.imp.gmail_service import GmailService
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

async def main():

    print("Hello, World!")
    if ACCESS_TOKEN:
        gmail_service = GmailService(ACCESS_TOKEN)
        mail = await gmail_service.get_gmail_thread_ids()
        mail_message = await gmail_service.get_mail_message_by_thread_id(mail["threadIds"][1])
        print(mail_message)
    else:
        print("ACCESS_TOKEN is not set")


if __name__ == "__main__":
    asyncio.run(main())
# source venv/bin/activate
# python app








