import re
from typing import List, Dict


def parse_articles_from_txt(text: str) -> List[Dict[str, str]]:
    article_pattern = re.compile(r"(?P<mark>[①-㊿])\s*(?P<content>.*)")
    chunks = []
    lines = text.splitlines()
    current_article = None
    buffer = []

    for line in lines:
        article_match = article_pattern.search(line)
        if article_match:
            if current_article:
                chunks.append({
                    "article_number": current_article["mark"],  
                    "article_title": "", 
                    "content": "\n".join(buffer).strip()
                })
                buffer = []
            current_article = {
                "mark": article_match.group("mark"),
                "content": article_match.group("content")
            }
            buffer.append(article_match.group("content"))
        elif current_article:
            buffer.append(line)

    if current_article:
        chunks.append({
            "article_number": current_article["mark"],
            "article_title": "",
            "content": "\n".join(buffer).strip()
        })

    return chunks
