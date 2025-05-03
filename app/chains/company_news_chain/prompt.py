from langchain_core.prompts import ChatPromptTemplate

# ニュース分類用プロンプトテンプレート
prompt_template = ChatPromptTemplate.from_template("""
あなたは、企業に関するニュース記事を評価・要約する優秀な分析アシスタントです。

以下に、ある企業に関連する複数の記事のタイトルと要約が与えられます。
各記事がポジティブな内容か、ネガティブな内容かを判断し、それぞれを分類しつつ、以下のスキーマに従ってJSON形式で出力してください。
また、これらの情報は、今後この企業に訪問した際の参考情報として使用されるため「就職」「転職」「社員の口コミ」といったキーワードが入った記事は削除してください。

対象企業名：{company_name}

記事一覧：
'''
{news_summaries}
'''

出力スキーマ：
{{
    "company_name": "string（会社名）",
    "positive_news": [
        {{
            "title": "string（記事タイトル）",
            "summary": "string（記事の内容要約）",
            "url": "string（記事のURL）"
        }}
    ],
    "negative_news": [
        {{
            "title": "string（記事タイトル）",
            "summary": "string（記事の内容要約）",
            "url": "string（記事のURL）"
        }}
    ]
}}

制約事項：
- 出力は **必ず** JSON形式で行ってください。日本語のコメントや説明を追加しないでください。
- ポジティブな内容とは、企業の成長、業績好調、新製品成功、提携・買収など前向きな話題を指します。
- ネガティブな内容とは、業績不振、訴訟、スキャンダル、リコール、炎上など問題性のある話題を指します。
""")