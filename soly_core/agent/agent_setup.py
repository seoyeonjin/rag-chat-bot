import json
import re
from typing import Optional,  List
from soly_core.agent.tools.faq_tool import faq_tool
from soly_core.agent.prompt import SYSTEM_PROMPT,chain
from soly_core.agent.tools.hwp_retriever_tool import hwp_search_tool


def extract_final_answer_and_summary(output: str) -> tuple[str, str]:
    output = output.strip()
    final_match = re.search(r"(?i)final answer:\s*", output)
    summary_match = re.search(r"(?i)summary:\s*", output)

    if final_match:
        answer_start = final_match.end()
        answer_end = summary_match.start() if summary_match else len(output)
        answer = output[answer_start:answer_end].strip()
        answer = re.split(r"(?i)\bsummary\s*:", answer)[0].strip()
    elif summary_match:
        answer = output[:summary_match.start()].strip()
    else:
        answer = output.strip()

    summary = (
        output[summary_match.end():].strip()
        if summary_match else "요약 없음"
    )

    return answer, summary


def run_with_summary(question: str, user_info: dict, history: Optional[List[str]]) -> tuple[str, str]:
    print(user_info)
    if hasattr(user_info, 'model_dump'):
        user_info = user_info.model_dump()
    elif isinstance(user_info, dict):
        user_info = user_info
    else:
        user_info = {}
    faq_result = faq_tool.func(question)
    hwp_result = hwp_search_tool.func(question)
    user_info_str = json.dumps(user_info, ensure_ascii=False, default=str)
    
    history_str = "\n".join(history or [])
    
    output = chain.invoke({
    "system_prompt": SYSTEM_PROMPT,
    "history": history_str,
    "question": question,
    "faq_result": faq_result,
    "hwp_result": hwp_result,
    "user_info": user_info_str
    })

    print(output)
    output_str = output.content if hasattr(output, "content") else str(output)
    return extract_final_answer_and_summary(output_str)
