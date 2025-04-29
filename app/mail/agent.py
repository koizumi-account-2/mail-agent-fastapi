from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from mail.models import MailAnalysisResult
from mail.prompts import prompt_template

class MailAnalysisAgent:
    def __init__(self,llm:ChatOpenAI):
        self.llm = llm.with_structured_output(MailAnalysisResult)

    def run(self, email_text: str) -> MailAnalysisResult:
        chain = (
            {"email_text": RunnablePassthrough()}  # 入力をそのまま email_text にマッピング
            | prompt_template                      # prompt_templateに渡す
            | self.llm                             # 構造化出力に渡す
        )
        result = chain.invoke(email_text)  # 直接 email_text を渡すだけでOK
        return result