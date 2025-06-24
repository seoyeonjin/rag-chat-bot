from soly_core.pipelines.hwp_to_chunks import load_hwp_chunks
from langchain_community.vectorstores import FAISS
from soly_core.model.bedrock_llm import embedding_model

file_path = "soly_core/data/2. (351400) 공급인증서 발급 및 거래시장 운영에 관한 규칙 전문_202409301.hwp"
chunks = load_hwp_chunks(file_path)

vectorstore = FAISS.from_documents(chunks, embedding_model)
vectorstore.save_local("soly_core/vectordb/hwp")
