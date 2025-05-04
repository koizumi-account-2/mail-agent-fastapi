from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from modules.config import model,tavily_retriever,ACCESS_TOKEN
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from chains.company.full_chain import CompanyInfoFullChain
from typing import Annotated,List    
import asyncio
from langchain_core.runnables import RunnableMap, RunnableLambda, RunnablePassthrough   
from chains.company.models import UserInfo
from features.mail.services.imp.gmail_service import GmailService
from features.calendar.models import CandidateDay,Slot
from chains.calendar.models import EventTrend
from datetime import datetime
import json
def funcA(inputs:dict):
    print(inputs)
    return inputs["AAA"]+"PPP"

async def main():

    # print("Hello, World!")
    # chain = (
    #     RunnableMap({
    #         "AAA": lambda x: "XXX",
    #         "BBB": lambda x: "YYY",
    #         "CCC": lambda x: "ZZZ",
    #     })
    # ).assign(anwser = funcA)
    # print(chain.invoke({"foo":"va"}))
    # return
    chain = CompanyInfoFullChain(llm=model, retriever=tavily_retriever)
    user_info = UserInfo(location="新宿駅") 
    print(await chain.run("損保ジャパン", user_info))
    return


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








