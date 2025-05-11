from fastapi import APIRouter
from chains.company.full_chain import CompanyInfoFullChain
from modules.config import model,tavily_retriever
from router.agent.schemas import CompanyInfoFullRequest


company_router = APIRouter()


@company_router.post("/")
async def get_company(request: CompanyInfoFullRequest):
    company_info_full_chain = CompanyInfoFullChain(model, tavily_retriever)
    result = await company_info_full_chain.run(request.company_name, request.user_info,request.company_address)
    return {
        "company_news": result["news"],
        "company_info": result["info"],
        "travel_time": result["travel_time"]
    }   
 