from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from features.mail.models import MailAnalysisResult, MailMessage
from features.mail.prompts import prompt_template

class MailAnalysisAgent:
    def __init__(self,llm:ChatOpenAI):
        self.llm = llm.with_structured_output(MailAnalysisResult)

    def run(self, email_messages: list[MailMessage], my_info: str, latest_message_id: str, existing_tasks: list[str], current_situation: str) -> MailAnalysisResult:
        
        email_result_str = "\n".join([
                f"メール送信者：{mail.sender}\n"
                f"メール本文：{mail.content}\n"
                f"メール日時：{mail.date}\n"
                f"メール件名：{mail.subject}\n"
                f"メールID：{mail.id}\n"
                for mail in email_messages
            ])
        existing_tasks_str = "\n".join([
            f"{task}\n"
            for task in existing_tasks
        ])
        chain = (   
            prompt_template                      # prompt_templateに渡す
            | self.llm                             # 構造化出力に渡す
        )
        result = chain.invoke({"email_result_str": email_result_str, "my_info": my_info,"latest_message_id": latest_message_id, "existing_tasks_str": existing_tasks_str, "current_situation": current_situation})  # 直接 email_text を渡すだけでOK
        return result