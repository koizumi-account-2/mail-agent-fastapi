from langchain_core.prompts import ChatPromptTemplate

# プロンプトテンプレート作成
from langchain.prompts import ChatPromptTemplate

# プロンプトテンプレート作成
prompt_template = ChatPromptTemplate.from_template("""
あなたは優秀なアシスタントです。

これから、メールスレッドを渡します。メールは時系列に並んでいるはずですが、その順番は必ずしも正しいとは限りません。メール日時も参考にしてください。
また、以前の分析結果の現在の状況も渡します。これは、messegeidが{latest_message_id}のメールの時点での状況です。current_situationが空の場合は、これが最初の分析です。
現在の状況：{current_situation}
そして、私は{my_info}です。
#######
以下のスキーマに沿ったJSONオブジェクトを作成してください。
スキーマ：
{{
    "tasks": [
        {{
            "task_name": "string（タスクの内容）",
            "assigned_to": "string（担当者の名前や部署など、明示的に指定されている場合。不明な場合は空文字）"
        }}
    ],
    "summary": "string（メールスレッドの内容を流れがわかるように要約し、さらにスレッド全体から読み取れる現在の状況（例：返事待ち、提案送付済み、日程調整中など）も含めて記述してください）"
}}

注意事項：
- tasksは、メールスレッドから読み取れる明示または暗示されている、今後対応すべきタスクや検討事項をリストアップしてください。なければ空リストで構いません。また、提示された解決済みのタスクはtasksに含めないでください。
- summaryはメールスレッドの内容を流れがわかるようにまとめ、現在の状況も明記してください。
- 出力は必ずJSON形式のみとし、余計なコメントや説明を付けないでください。

メールスレッド：
'''
{email_result_str}
'''
解決済みのタスク：
'''
{existing_tasks_str}
'''
                                                   
""")