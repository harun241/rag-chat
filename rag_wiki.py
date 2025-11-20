import wikipedia

def wiki_local_rag(query):
    try:
        summary = wikipedia.summary(query, sentences=3)
        return summary
    except Exception as e:
        return f"Error fetching from Wikipedia: {e}"
