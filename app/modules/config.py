from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.retrievers import TavilySearchAPIRetriever
import os

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")
# print("api_key",api_key)
model = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)

use_dummy = os.getenv("USE_DUMMY") == "true"

tavily_api_key = os.getenv("TAVILY_API_KEY")
tavily_retriever = TavilySearchAPIRetriever(api_key=tavily_api_key, time_range="month")