from fastapi import APIRouter
from chains.company.full_chain import CompanyInfoFullChain
from modules.config import model,tavily_retriever
from router.agent.schemas import CompanyInfoFullRequest
company_router = APIRouter()


@company_router.post("/")
async def get_company(request: CompanyInfoFullRequest):
    print("company_name",request.  company_name)
    print("user_info",request.user_info)
    company_info_full_chain = CompanyInfoFullChain(model, tavily_retriever)
    result = await company_info_full_chain.run(request.company_name, request.user_info)
    return {
        "company_news": result[0],
        "company_info": result[1],
        "travel_time": result[2]
    }   