from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from modules.config import model,tavily_retriever
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from chains.full_chain import CompanyInfoFullChain
from typing import Annotated
import asyncio
@tool
def add(
    a: Annotated[int, '一つ目の値'],
    b: Annotated[int, '二つ目の値'],
) -> int:
    """2つの値を足し算して返す"""
    return a + b
@tool
def minus(
    a: Annotated[int, '一つ目の値'],
    b: Annotated[int, '二つ目の値'],
) -> int:
    """2つの値を引き算して返す"""
    return a - b

@tool
def getMails(
    thread_id: Annotated[str, 'threadのid']
) -> list[str]:
    """
    thread_idに紐づいたメールのメッセージ一覧を取得する
    """
    if thread_id == "A123":
        return [
            "明日は資料のコピーをよろしくお願いします"
        ]
    else:
        return []


@tool
def addTask(
    thread_id: Annotated[str, 'threadのid'],
    project_id: Annotated[str, 'projectのid'],
    task_name: Annotated[str, 'taskの名前'],
) -> int:
    """
    thread_idとproject_idとtask_nameを受け取り、taskを作成する
    thread_idが指定されない場合には、thread_idを空文字にする
    """
    print(f"thread_id: {thread_id}, project_id: {project_id}, task_name: {task_name}")
    return "taskを作成しました"

async def main():
    print("Hello, World!")

    company_info_full_chain = CompanyInfoFullChain(model, tavily_retriever)
    result = await company_info_full_chain.run("損保ジャパン")
    print(result)


    # プロンプトの定義
    # prompt = ChatPromptTemplate.from_messages(
    #     [
    #         (
    #             'system',
    #             '与えられたinputに従って処理を呼び出してください',
    #         ),
    #         ('human', '{input}'),
    #         # Placeholders fill up a **list** of messages
    #         ('placeholder', '{agent_scratchpad}'),
    #     ]
    # )

    # # エージェントを作成
    # agent = create_tool_calling_agent(model, [add, minus, addTask, getMails], prompt)

    # # エージェントを実行
    # agent_executor = AgentExecutor(agent=agent, tools=[add, minus, addTask, getMails])
    # result = agent_executor.invoke({'input': 'メールのメッセージを取得して、タスクを洗い出し、作成してください。補足情報：project_id: 456,thread_id: A123'})
    # print(result)

if __name__ == "__main__":
    asyncio.run(main())
# source venv/bin/activate
# python app








