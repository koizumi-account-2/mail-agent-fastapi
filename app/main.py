from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from features.mail.agent import MailAnalysisAgent
from features.mail.models import MailMessage
from modules.config import model
from router.auth.mail import mail_router
from router.agent.company import company_router
from exceptions import http_exception_handler, validation_exception_handler, generic_exception_handler
app = FastAPI()
# カスタム例外ハンドラーの登録
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # セキュリティのため本番では特定のドメインに限定する
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# mail系
app.include_router(mail_router, prefix="/api/auth/mail")
# company系
app.include_router(company_router, prefix="/api/agent/company")

@app.get("/api/health")
async def health():
    return {"message": "ok"}

# メールの分析
# どこまでのメールを分析したかわかるように、latest_message_idを渡す
# latest_message_idに紐づいているタスクも渡す。例えば、作成されたtaskや消化されたタスク
@app.post("/api/mail/analyze")
async def mail_analyze(request: Request):
    body = await request.json()
    email_messages = [MailMessage(**message) for message in body["email_messages"]]
    current_situation = body["current_situation"]
    print("current_situation",current_situation)
    my_info = body["my_info"]
    latest_message_id = current_situation["latest_message_id"]
    existing_tasks = current_situation["existing_tasks"]
    my_info = "A株式会社 営業部 A"
    # url = "http://localhost:3000/api/task"
    # payload = {
    #     "projectId": 1,
    #     "threadId": "1967b4ce72534cf7",
    # }

    # async with httpx.AsyncClient() as client:
    #     response = await client.post(url, json=payload)
    #     print(response.json())
    agent = MailAnalysisAgent(llm = model)
    result = agent.run(email_messages=email_messages, my_info=my_info, latest_message_id=latest_message_id, existing_tasks=existing_tasks, current_situation=current_situation)
    return result
# uvicorn main:app --reload

# A様

# ご連絡ありがとうございます。
# 5月2日（木）15時より、よろしくお願い申し上げます。

# 当日、事前にお送りいただく資料などございましたら、
# お手数ですが共有いただけますと幸いです。

# それでは、引き続きどうぞよろしくお願いいたします。

# ---
# B株式会社
# 営業推進部　B
# 電話番号：XXX-XXXX-XXXX
# メール：b@example.com

# 2025年4月28日(月) 16:30 小泉舜敬 <nisikana.suibu318@gmail.com>:


# B様

# お世話になっております。Aです。

# ご連絡いただきありがとうございます。
# 5月2日（木）15:00〜16:00にて、ぜひお願いできればと存じます。

# 当日は、Zoomにてご説明させていただきますので、
# 前日に招待URLをお送りいたします。

# どうぞよろしくお願いいたします。

# ---
# A株式会社
# 営業部　A
# 電話番号：XXX-XXXX-XXXX
# メール：a@example.com

# 2025年4月28日(月) 16:29 小泉舜敬 <koizumi.yoshitaka.mx@gmail.com>:
# A様

# いつも大変お世話になっております。B株式会社のBです。

# ご提案の件、ぜひ詳しくお話を伺いたく存じます。
# 以下の日程であれば調整可能ですが、ご都合いかがでしょうか。

# - 5月2日（木）10:00〜11:00
# - 5月2日（木）15:00〜16:00
# - 5月7日（火）11:00〜12:00

# ご確認のうえ、ご希望の時間帯をお知らせください。
# 引き続き、どうぞよろしくお願いいたします。

# ---
# B株式会社
# 営業推進部　B
# 電話番号：XXX-XXXX-XXXX
# メール：b@example.com

# 2025年4月28日(月) 16:29 小泉舜敬 <nisikana.suibu318@gmail.com>:
# B様

# いつもお世話になっております。A株式会社のAでございます。

# このたび、弊社にて進めております「〇〇プロジェクト」について、
# 御社にご協力いただけないかと思いご連絡させていただきました。

# お手すきの際に、ぜひ一度、オンラインにて詳細のご説明をさせていただければと考えております。
# ご都合のよろしい日程をいくつかご教示いただけますでしょうか。

# 何卒よろしくお願い申し上げます。

# ---
# A株式会社
# 営業部　A
# 電話番号：XXX-XXXX-XXXX
# メール：a@example.com
