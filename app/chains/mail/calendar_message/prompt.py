from langchain.prompts import ChatPromptTemplate

calendar_message_prompt = ChatPromptTemplate.from_template("""
以下の候補日程をもとに、調整相手に送るための丁寧な日本語のメールを作成してください。

# 候補日程一覧
{draft}

# メール文の要件
- 1文目で挨拶と目的を述べる（例：「お世話になっております。〇〇の日程についてご相談させてください。」）
- 箇条書きで候補を提示する
- 返信のお願いで締める（例：「ご都合のよい日時をお知らせいただけますと幸いです。」）
- 丁寧語・敬語を使う
- 件名や署名は不要です
""")