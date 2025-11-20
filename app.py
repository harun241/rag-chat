import wikipedia
import re

def clean_query(query):
    """
    Clean the user query to extract main topic for Wikipedia search.
    """
    query = query.lower()
    query = re.sub(r"what do you know by the name|tell me about|who is|explain|define", "", query)
    return query.strip().title()

def wiki_local_rag(query):
    """
    Search Wikipedia and return a readable summary.
    """
    query = clean_query(query)
    try:
        results = wikipedia.search(query)
        if not results:
            return "Sorry, I could not find anything on Wikipedia for your query."

        top_page = results[0]
        summary = wikipedia.summary(top_page, sentences=5)
        return summary

    except wikipedia.DisambiguationError as e:
        summary = wikipedia.summary(e.options[0], sentences=5)
        return summary

    except Exception as e:
        return f"Error fetching from Wikipedia: {e}"

def run_bot():
    print("Welcome to Wikipedia Bot! Type 'exit' to quit.\n")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break
        answer = wiki_local_rag(query)
        print("\nBot:", answer, "\n")

if __name__ == "__main__":
    run_bot()
