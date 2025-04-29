from langchain_core.prompts import ChatPromptTemplate

# プロンプトテンプレート作成
from langchain.prompts import ChatPromptTemplate

# プロンプトテンプレート作成
prompt_template = ChatPromptTemplate.from_template("""
あなたは優秀なアシスタントです。

これから、メールスレッド内の1通のメール本文を渡します。

以下のスキーマに沿ったJSONオブジェクトを作成してください。

スキーマ：

{{
  "tasks": (list of string) メール本文から読み取れる、今後対応すべきタスクや検討事項をリストアップしてください。
  "summary": (string) メール本文の内容を要約し、さらにスレッド全体から読み取れる現在の状況（例：返事待ち、提案送付済み、日程調整中など）も含めて記述してください。
}}

注意事項：
- tasksは、本文から明示または暗示されているタスクを列挙してください。なければ空リストで構いません。
- summaryは本文の要点を簡潔にまとめ、現在の状況も明記してください。
- 出力は必ずJSON形式のみとし、余計なコメントや説明を付けないでください。

入力メール本文：

'''
{email_text}
'''
""")