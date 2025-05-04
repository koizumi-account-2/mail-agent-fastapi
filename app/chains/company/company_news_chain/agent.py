from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import TavilySearchAPIRetriever
from chains.company.models import CompanyNewsAnalysisResult
from chains.company.company_news_chain.prompt import prompt_template
from langchain_core.runnables import Runnable
import json
class CompanyNewsSearchAgent:
    def __init__(self, llm: ChatOpenAI, retriever: TavilySearchAPIRetriever):
        self.llm = llm
        self.retriever = retriever
        self.parser = PydanticOutputParser(pydantic_object=CompanyNewsAnalysisResult)
        self.chain = self._build_chain()

    def _fetch_news(self, company_name: str) -> CompanyNewsAnalysisResult:
        # 検索クエリ定義
        # --- クエリ ---
        positive_query = f"{company_name} 業績好調 OR 成長 OR 株価上昇 OR 提携"
        negative_query = f"{company_name} 不祥事 OR リコール OR 訴訟 OR 炎上 OR 不振"


        positive_docs = self.retriever.invoke(
            positive_query
        )[:5]

        negative_docs = self.retriever.invoke(
            negative_query
        )[:5]



        def doc_to_dict(doc):
            return {
                "title": doc.metadata.get("title", "不明"),
                "summary": doc.page_content,
                "url": doc.metadata.get("source", "")
            }

        result = {
            "company_name": company_name,
            "positive_news": [doc_to_dict(doc) for doc in positive_docs],
            "negative_news": [doc_to_dict(doc) for doc in negative_docs]
        }

        return json.dumps(result, ensure_ascii=False, indent=2)


    def _build_chain(self) -> Runnable:
        """
        company_name を入力に取り、Tavily検索 + フォーマット + プロンプト + LLM + パースを含む LCELチェーンを返す
        """
        def prepare_inputs(input: dict):
            company_name = input["company_name"]
            summaries = self._fetch_news(company_name)

            return {
                "company_name": company_name,
                "news_summaries": summaries
            }

        chain = (
            RunnableLambda(prepare_inputs)
            | prompt_template
            | self.llm
            | self.parser
        )
        return chain
    def get_chain(self) -> Runnable:
        return self.chain