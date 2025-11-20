import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def google_rag_answer(query):
    # 1. Google search URLs
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    links = [a['href'].split("/url?q=")[1].split("&")[0] for a in soup.select('a') if "url?q=" in a.get('href', '')][:3]

    if not links:
        return "No URLs found from Google."

    # 2. Scrape page content
    texts = []
    for url in links:
        try:
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")
            paragraphs = soup.find_all("p")
            text = " ".join([p.get_text() for p in paragraphs])
            texts.append(text)
        except:
            continue

    if not texts:
        return "No content found from Google."

    # 3. Embedding & retrieve best match
    query_emb = model.encode(query)
    doc_embs = model.encode(texts)
    scores = util.cos_sim(query_emb, doc_embs)
    best_doc = texts[scores.argmax()]

    # 4. Return first 500 chars
    return best_doc[:500]
