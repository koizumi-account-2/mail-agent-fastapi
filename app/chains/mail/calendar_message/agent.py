from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from langchain_core.runnables import Runnable
from features.calendar.services.common_calendar_service import CandidateDay
from typing import List
from chains.mail.calendar_message.prompt import calendar_message_prompt



class CalendarMessageAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.parser = StrOutputParser()
        self.chain = self._build_chain()

    def _format_slot_summary(self,days: List[CandidateDay]) -> str:
        print("days",days)
        summary = []
        for day in days:
            dow_label = ["月", "火", "水", "木", "金", "土", "日"][day.day_of_week]
            date_label = day.date.strftime(f"%m月%d日（{dow_label}）")
            for slot in sorted(day.candidates, key=lambda s: s.start):
                start_str = slot.start.strftime("%H:%M")
                end_str = slot.end.strftime("%H:%M")
                summary.append(f"- {date_label} {start_str}〜{end_str}")
        return "\n".join(summary)





    def _build_chain(self) -> Runnable:
        def prepare_inputs(candidate_days: List[CandidateDay]):
            print("candidate_days",candidate_days)
            draft = self._format_slot_summary(candidate_days)
            return {
                "draft": draft
            }

        chain = (
            RunnableLambda(prepare_inputs)
            | calendar_message_prompt
            | self.llm
            | self.parser
        )
        return chain
    def get_chain(self) -> Runnable:
        return self.chain