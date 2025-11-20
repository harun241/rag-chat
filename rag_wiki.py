import wikipedia
import re

def clean_query(query):
    """
    Clean the user query to extract main topic for Wikipedia search.
    """
    # Remove common phrases
    query = query.lower()
    query = re.sub(r"what do you know by the name|tell me about|who is|explain|define", "", query)
    return query.strip().title()  # Capitalize for Wikipedia search

def wiki_local_rag(query):
    query = clean_query(query)  # use the cleaning function
    try:
        # Search Wikipedia for relevant pages
        results = wikipedia.search(query)
        if not results:
            return "No relevant Wikipedia page found."
        
        # Take the top search result
        top_page = results[0]
        summary = wikipedia.summary(top_page, sentences=3)
        return summary
    
    except wikipedia.DisambiguationError as e:
        # If multiple pages match, choose the first option
        summary = wikipedia.summary(e.options[0], sentences=3)
        return summary

    except Exception as e:
        return f"Error fetching from Wikipedia: {e}"
