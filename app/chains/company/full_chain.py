from chains.company.company_news_chain.agent import CompanyNewsSearchAgent
from chains.company.company_info_chain.agent import CompanyInfoSearchAgent
from langchain_core.runnables import RunnableParallel
from modules.config import model,tavily_retriever,use_dummy


from chains.company.company_news_chain.models import CompanyNewsAnalysisResult,NewsArticle
from chains.company.company_info_chain.models import CompanyInfoAnalysisResult

# CompanyInfoAnalysisResult のダミーデータ
dummy_info = CompanyInfoAnalysisResult(
    company_name="損保ジャパン",
    location="東京都新宿区西新宿1-26-1",
    industry="保険業",
    business_content="自動車保険、火災保険、地震保険、海外旅行保険などの保険商品を提供",
    employee_number=20767
)

# CompanyNewsAnalysisResult のダミーデータ
dummy_news = CompanyNewsAnalysisResult(
    company_name="損保ジャパン",
    positive_news=[
        NewsArticle(
            title="【損害保険：業界研究】大手4社（東京海上日動火災保険・損害保険ジャパン・三井住友海上火災保険・あいおいニッセイ同和損害保険）を比較!業績比較 ...",
            summary="これらの地域は、将来的な経済成長が期待され、保険の普及率がまだ低いことから、今後の市場拡大が見込まれています。日本の損害保険会社は、長年培ってきた保険の仕組みやノウハウを生かし、これらの地域でのシェア拡大を目指しています。",
            url="https://www.onecareer.jp/articles/836"
        ),
        NewsArticle(
            title="損保ジャパン - sompo-japan.jp",
            summary="当社は、一連の問題に端を発し、2024年2月末に金融庁から受けた業務改善命令や自然災害の頻発化・激甚化等の環境変化を踏まえ、5月28日(火)に、2024年度を開始年度とする新中期経営計画を公表しました。. 新中期経営計画では、「お客さま、社会、そして自分にまっすぐ。",
            url="https://www.sompo-japan.jp/company/initiatives/sjr/"
        ),
        NewsArticle(
            title="2024年度 - 【公式】損保ジャパン",
            summary="損保ジャパンの公式ウェブサイトです。すべてをお客さまの立場で考える会社を目指し、自動車保険、火災保険、地震保険、海外旅行保険など、安心・安全・健康をサポートする商品・サービスを多数取り扱っています。",
            url="https://www.sompo-japan.co.jp/news/2024/"
        )
    ],
    negative_news=[
        NewsArticle(
            title="急成長のビッグモーターのわがままに屈した大手損保―損保ジャパン",
            summary="金融庁は2024年1月25日、ビッグモーターと取引を継続していたSOMPOホールディングスと傘下の損保ジャパンに業務改善命令を発した。他の損保会社が取引を停止していた中で、同社の中ではどんな意思決定が下されていたのか。",
            url="https://project.nikkeibp.co.jp/HumanCapital/atcl/column/00079/030800013/"
        ),
        NewsArticle(
            title="損保ジャパン「過失割合10対0でも払ってもらえない」対応がずさん過ぎると炎上",
            summary="今回の損保ジャパンの炎上は、12月10日～17日までの1週間を見ても、12日から急激に伸びています。大きな報道があったわけでもなく、市民の",
            url="https://nlab.itmedia.co.jp/research/articles/3450/"
        ),
        NewsArticle(
            title="損保ジャパン、顧客情報7万件流出か サイバー攻撃で - 日本経済新聞",
            summary="損害保険ジャパンは1日、業務委託先がサイバー攻撃を受けたことで、約7万5000件の顧客情報が流出した可能性があると発表した。",
            url="https://www.nikkei.com/article/DGXZQOUB017PG0R00C25A5000000/"
        ),
        NewsArticle(
            title="損保ジャパン、事故調査の顧客情報が漏えいの可能性 - Yahoo!ニュース",
            summary="損害保険ジャパンは5月1日、業務委託先がサイバー攻撃を受けたことで、顧客の事故調査に関する情報が漏えいした可能性があると発表した。",
            url="https://news.yahoo.co.jp/articles/f056ad47c02fcc5e1a1c69b429e97d0e8d69617e"
        )
    ]
)

class CompanyInfoFullChain:
    def __init__(self, llm, retriever):
        self.news_agent = CompanyNewsSearchAgent(llm=llm, retriever=retriever)
        self.info_agent = CompanyInfoSearchAgent(llm=llm, retriever=retriever)
        self.chain = self._build_chain()
        self.use_dummy = use_dummy

    def _build_chain(self):
        return RunnableParallel({
            "news": self.news_agent.get_chain(),
            "info": self.info_agent.get_chain()
        })

    async def run(self, company_name):
        if self.use_dummy:
            return dummy_news, dummy_info
        else:
            return await self.chain.ainvoke({"company_name": company_name})
    
