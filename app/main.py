from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  
from langchain_openai import ChatOpenAI
from mail.agent import MailAnalysisAgent
from modules.config import model
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # セキュリティのため本番では特定のドメインに限定する
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"message": "ok"}


@app.post("/api/mail/analysis")
async def mail_analysis(request: Request):
    body = await request.json()
    email_text = body["email_text"]
    agent = MailAnalysisAgent(llm = model)
    result = agent.run(email_text=email_text)
    return {"result": result}
# uvicorn main:app --reload