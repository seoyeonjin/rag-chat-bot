
from langchain_core.output_parsers import StrOutputParser
from soly_core.model.bedrock_llm import llm
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

SYSTEM_PROMPT = (
    "당신은 태양광 발전소 운영자를 도와주는 AI 상담원입니다.\n"
    "질문에 대한 답변을 바로 생성하세요. 절대 추론 단계(Thought, Action, Observation)를 출력하지 마세요.\n"
    "그냥 사용자에게 직접 답변만 하세요.\n\n"
    "응답은 반드시 아래 형식을 따라야 합니다:\n\n"
    "Final Answer: (정중하고 간결한 전체 응답)\n"
    "Summary: (핵심 요약)\n\n"
    "각 문장을 하나씩 순차적으로 생성하세요. 한 번에 전체 응답을 생성하지 마세요."
)

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("{system_prompt}"),
    HumanMessagePromptTemplate.from_template(
        "[대화 이력]\n{history}\n\n"
        "[질문]\n{question}\n\n"
        "[FAQ 검색 결과]\n{faq_result}\n\n"
        "[규칙 검색 결과]\n{hwp_result}\n\n"
        "[사용자 정보]\n{user_info}\n\n"
        "Final Answer:"
    )
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser
