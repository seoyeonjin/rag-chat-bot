from langchain.tools import Tool
from langchain.chains import RetrievalQA
from soly_core.model.bedrock_llm import llm, embedding_model
from langchain_community.vectorstores import FAISS

faq_vectorstore = FAISS.load_local(
    "soly_core/vectordb/faq",
    embedding_model,
    allow_dangerous_deserialization=True
)

faq_qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=faq_vectorstore.as_retriever()
)

def faq_tool_func(question: str) -> str:
    query = f"FAQ에 있는 질문 중 관련 있는 항목을 찾아주세요. 사용자 질문: {question}"
    docs = faq_vectorstore.similarity_search(query, k=3)
    print("📚 검색된 FAQ 문서:", docs[0].page_content if docs else "없음")
    return faq_qa_chain.invoke(f"다음 질문에 한국어로 답변해 주세요: {query}")

faq_tool = Tool(
    name="faq_search_tool",
    func=faq_tool_func,
    description="오솔라 서비스에 대한 자주 묻는 질문을 검색하는 도구입니다."
)
