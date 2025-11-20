from flask import Flask, request, jsonify
from rag_wiki import wiki_local_rag


app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"answer": "No query provided."})

    answer = wiki_local_rag(query)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
