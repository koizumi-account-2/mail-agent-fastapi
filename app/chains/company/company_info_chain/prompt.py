from langchain_core.prompts import ChatPromptTemplate

company_info_prompt = ChatPromptTemplate.from_template("""
あなたは優秀な企業情報アナリストです。以下に提示するニュース記事の要約や企業ページから、対象企業の基本情報を抽出してください。

対象企業名：{company_name}

参考情報：
'''
{company_info_snippets}
'''

出力形式：
{{
    "company_name": "string",
    "location": "string",
    "industry": "string",
    "business_content": "string",
    "employee_number": int
}}

制約事項：
- 出力は **必ず** JSON形式で返してください。
- 数値項目（特に従業員数）は、数値で返してください。
- 不明な場合は「不明」と出力してください。従業員数が不明な場合は0と出力してください。
- 英語ではなく**日本語**で出力してください。
""")