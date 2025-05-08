from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import TavilySearchAPIRetriever
from chains.company.models import CompanyInfoAnalysisResult
from chains.company.company_info_chain.prompt import company_info_prompt
from langchain_core.runnables import Runnable

class CompanyInfoSearchAgent:
    def __init__(self, llm: ChatOpenAI, retriever: TavilySearchAPIRetriever):
        self.llm = llm
        self.retriever = retriever
        self.parser = PydanticOutputParser(pydantic_object=CompanyInfoAnalysisResult)
        self.chain = self._build_chain()

    def _fetch_info(self, company_name: str) -> str:
        query = f"{company_name} 会社概要 OR 事業内容 OR 業種 OR 所在地 OR 従業員数"

        docs = self.retriever.invoke(query)[:5]

        def format_doc(doc):
            return f"タイトル: {doc.metadata.get('title', '不明')}\n要約: {doc.page_content}\nURL: {doc.metadata.get('source', '')}"

        return "\n---\n".join([format_doc(doc) for doc in docs])

    def _build_chain(self) -> Runnable:
        def prepare_inputs(company_name: str):
            info = self._fetch_info(company_name)
            print("info",info)
            return {
                "company_name": company_name,
                "company_info_snippets": info
            }

        return (
            RunnableLambda(prepare_inputs)
            | company_info_prompt
            | self.llm
            | self.parser
        )
    def get_chain(self) -> Runnable:
        return self.chain
