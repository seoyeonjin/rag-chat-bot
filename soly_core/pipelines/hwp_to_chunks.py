from soly_core.pipelines.hwp_to_documents import load_hwp_and_parse
from soly_core.chunking.text_splitter import get_text_splitter
from langchain.schema import Document
from typing import List

def load_hwp_chunks(file_path: str) -> List[Document]:
    docs = load_hwp_and_parse(file_path)
    splitter = get_text_splitter()
    return splitter.split_documents(docs)