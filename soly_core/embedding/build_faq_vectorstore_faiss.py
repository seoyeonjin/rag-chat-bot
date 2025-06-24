from langchain.vectorstores import FAISS
from langchain_core.documents import Document
import json
import os
from soly_core.model.bedrock_llm import embedding_model


with open("soly_core/data/osolar_faq.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

faq_documents = []
for item in faq_data:
    content = f"Q: {item['question']}\nA: {item['answer']}"
    metadata = {"category": item["category"]}
    faq_documents.append(Document(page_content=content, metadata=metadata))

print(f"총 {len(faq_documents)}개 문서 변환 완료")
print(f"예시:\n{faq_documents[0].page_content}")

persist_path = "./soly_core/vectordb/faq"

os.makedirs(persist_path, exist_ok=True)

vectorstore = FAISS.from_documents(faq_documents, embedding_model)
vectorstore.save_local(persist_path)

print(f"FAISS 인덱스 저장 완료: {persist_path}")
