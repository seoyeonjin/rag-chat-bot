from langchain_community.vectorstores import FAISS
from langchain.tools import Tool
from soly_core.model.bedrock_llm import embedding_model

retriever = FAISS.load_local(
    "soly_core/vectordb/hwp",
    embedding_model,
    allow_dangerous_deserialization=True
).as_retriever()

def search_hwp_knowledge(query: str) -> str:
    docs = retriever.invoke(query)
    if not docs:
        return "해당 질문에 대한 관련 규칙을 찾을 수 없습니다."

    formatted = []
    for doc in docs:
        article = doc.metadata.get("article_number", "알 수 없음")
        title = doc.metadata.get("article_title", "")
        content = doc.page_content.strip()

        formatted.append(f"[{article} {title}]\n{content}")

    return "\n\n".join(formatted)

hwp_search_tool = Tool(
    name="hwp_search_tool",
    func=search_hwp_knowledge,
    description=(
        "공급인증서 발급 및 거래시장 운영에 관한 규칙에서 질의에 대한 관련 내용을 찾아줍니다.\n"
        "예: '인증서 유효기간은 어떻게 되나요?', 'REC 발급 기준이 뭐야?'"
    )
)
