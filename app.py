from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import requests
import json

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["Movies"]
collection = db["movie_dataset"]


# Convert Natural Language to MongoDB Query using Ollama
def generate_query(user_input):

    prompt = f"""
You are a MongoDB query generator.

Return ONLY valid JSON.
Do not explain anything.
Do not add backticks.
Do not add text before or after JSON.

Schema:
- genres.name
- keywords.name
- vote_average
- runtime
- original_language

Examples:

Input: Action movies
Output: {{ "genres.name": "Action" }}

Input: Movies above rating 8
Output: {{ "vote_average": {{ "$gt": 8 }} }}

User Query: {user_input}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma:7b",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()["response"]

    # CLEAN THE OUTPUT
    result = result.strip()
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    return result

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    user_input = request.form["query"]

    mongo_query_text = generate_query(user_input)

    try:
        mongo_query = json.loads(mongo_query_text)
    except Exception as e:
        print("Model Output:", mongo_query_text)  # DEBUG
        return jsonify({"error": "Model returned invalid JSON"})

    results = list(collection.find(
        mongo_query,
        { "_id": 0, "title": 1 }
    ).limit(20))

    movie_titles = [movie["title"] for movie in results]

    return jsonify(movie_titles)


if __name__ == "__main__":
    app.run(debug=True)
