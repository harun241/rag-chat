import wikipedia
import re

# --- Dataset loading ---
def load_dataset(file_path="questions.txt"):
    dataset = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "|" not in line:
                continue
            question, answer = line.split("|", 1)
            dataset.append({"question": question.strip(), "answer": answer.strip()})
    return dataset

dataset = load_dataset()

# --- Query cleaning ---
def clean_query(query):
    query = query.lower()
    query = re.sub(r"what do you know by the name|tell me about|who is|explain|define", "", query)
    return query.strip().title()

# --- Dataset search (partial/keyword match) ---
def search_dataset(query):
    query_words = set(query.lower().split())
    best_match = None
    max_overlap = 0
    for item in dataset:
        question_words = set(item["question"].lower().split())
        overlap = len(query_words & question_words)
        if overlap > max_overlap:
            max_overlap = overlap
            best_match = item["answer"]
    # Return answer if at least 1 word matches
    if max_overlap > 0:
        return best_match
    return None

# --- Greetings handling ---
def handle_greetings(query):
    greetings = ["hello", "hi", "hey", "good morning", "good evening"]
    if query.lower() in greetings:
        return "Hello! How can I help you today?"
    if "how are you" in query.lower():
        return "I'm just a bot, but I'm doing great! How about you?"
    return None

# --- Main bot function ---
def wiki_local_rag(query):
    # Check greetings first
    greet_reply = handle_greetings(query)
    if greet_reply:
        return greet_reply

    # Check dataset
    dataset_answer = search_dataset(query)
    if dataset_answer:
        return dataset_answer

    # Wikipedia fallback
    query_clean = clean_query(query)
    try:
        results = wikipedia.search(query_clean)
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

# --- Interactive console ---
if __name__ == "__main__":
    print("Welcome! Type 'exit' to quit.\n")
    while True:
        query = input("You: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break
        answer = wiki_local_rag(query)
        print("Bot:", answer, "\n")
