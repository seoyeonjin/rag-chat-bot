from soly_core.loader.hwp_loader import HWPLoader
from langchain.schema import Document
from soly_core.preprocessors.hwp_parser import parse_articles_from_txt
from typing import List
import re

def clean_text(text: str) -> str:
    text = re.sub(r"\s*공급인증서 발급 및 거래시장 운영에 관한 규칙\s*", "", text)
    return text

def load_hwp_and_parse(file_path: str) -> List[Document]:
    loader = HWPLoader(file_path)
    raw_text = next(loader.lazy_load()).page_content
    raw_text = clean_text(raw_text)
    parsed_chunks = parse_articles_from_txt(raw_text)
    return [
        Document(
            page_content=chunk["content"],
            metadata={
                "article_number": chunk["article_number"],
                "article_title": chunk["article_title"],
                "source": file_path
            }
        )
        for chunk in parsed_chunks
    ]