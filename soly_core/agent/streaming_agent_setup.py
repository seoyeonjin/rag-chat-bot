import json
from soly_core.agent.tools.faq_tool import faq_tool
from soly_core.agent.tools.hwp_retriever_tool import hwp_search_tool
from soly_core.agent.streaming_prompt import chain, SYSTEM_PROMPT

async def stream_with_summary(question: str, user_info: dict, history: list[str]):
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
    input_vars = {
        "system_prompt": SYSTEM_PROMPT,
        "question": question,
        "faq_result": faq_result,
        "hwp_result": hwp_result,
        "user_info": user_info_str,
        "history": history_str
    }

    async for chunk in chain.astream(input_vars):
        yield chunk.content if hasattr(chunk, "content") else str(chunk)
        
def stream_with_summary_sync(question: str, user_info: dict, history: list[str]):
    faq_result = faq_tool.func(question)
    hwp_result = hwp_search_tool.func(question)
    user_info_str = json.dumps(user_info, ensure_ascii=False, default=str)
    history_str = "\n".join(history or [])
    input_vars = {
        "system_prompt": SYSTEM_PROMPT,
        "question": question,
        "faq_result": faq_result,
        "hwp_result": hwp_result,
        "user_info": user_info_str,
        "history": history_str
    }

    for chunk in chain.stream(input_vars): 
        yield chunk.content if hasattr(chunk, "content") else str(chunk)