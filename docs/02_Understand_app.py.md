## Understanding the code behind _Qory_
In this document, I'll try my best to explain the code in _app.py_.

First, we import all the modules and libraries required for the project.
```
from flask import Flask, request, jsonify, render_template
```
Here we are importing all the modules required from _Flask_.
- Flask: the main class used to create a Flask application instance.
- request: used to access incoming HTTP request data (like form input or JSON payload).
- jsonify: a helper function that converts Python objects (like lists or dictionaries) into JSON responses to return to the browser.
- render_template: used to render HTML files stored in the templates folder. This allows dynamic content in the frontend.

```
from pymongo import MongoClient
```
Here, we are connecting our Python app to our database in MongoDB.

```
import requests
```
`requests` is a python library to make HTTPS requests. Here, it’s used to send POST requests to your local Ollama API (gemma:7b) to convert natural language queries into MongoDB queries.

```
import json
```
`json` is a Python’s built-in library for working with JSON (JavaScript Object Notation). Used here to parse JSON returned by Ollama and to convert Python objects to JSON when returning responses to the browser.

```
app = Flask(__name__)
```
Creates a new Flask app instance.`__name__` is a special Python variable representing the module name. Flask uses it to locate templates, static files, etc.

```
client = MongoClient("mongodb://localhost:27017/")
```
Connects to your local MongoDB server running on port 27017.

```
db = client["Movies"]
```
Access the database named "Movies" from your MongoDB instance and store it in the variable _db_.

```
collection = db["movie_dataset"]
```
Access the collection called "movie_dataset" inside the "Movies" database. Now, stored in variable _collection_.

```
def generate_query(user_input):
```
- Defines a Python function named **generate_query**.
- It takes one argument: **user_input** which is a string typed by the user in natural language (like “Action movies above rating 7”).
- Purpose: send this string to Ollama AI and get a MongoDB query JSON in return.

```
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
```
- This is a **multiline f-string prompt** for Ollama.
- It tells the AI exactly what to do:
   - Generate MongoDB queries.
   - Output only valid JSON (no explanations, no markdown).
   - Provides the database schema so the AI knows which fields exist.
   - Gives examples to guide the AI’s output.
   - Inserts the actual user query at the bottom ({user_input}) for Ollama to process.
- We are basically instructing it to provide as correct of a response as it could.

```
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma:7b",
            "prompt": prompt,
            "stream": False
        }
    )
```
- This sends a **POST request** to the local Ollama server running on port 11434.
- JSON payload sent:
     - "model": "gemma:7b" → uses the 7B Gemma model.
     - "prompt": prompt → the prompt string we just defined.
     - "stream": False → we want the entire response at once, not a streamed chunk.
- The response object now contains the output from Ollama.

```
result = response.json()["response"]
```
- Converts the HTTP response from Ollama to a **Python dictionary** using .json().
- Extracts the _response_ field, which is the **raw JSON text of the MongoDB query** returned by the AI.

```
    # CLEAN THE OUTPUT
    result = result.strip()
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()
```
- This is used to clean up the AI's output:
     - `.strip()`removes extra spaces or newlines at the start/end.
     - `.replace("```json", "")` and `.replace("```", "")` remove any leftover code block markers (sometimes Gemma outputs json or ).
- Ensures we have pure JSON string ready to parse.

```
return result
```
Returns the cleaned JSON string representing the MongoDB query.

```
@app.route("/")
def home():
    return render_template("index.html")
```
This renders the `index.html` file when the website is first opened. Whenever the URL has `http://127.0.0.1:5000/`, the home page is displayed.

```
@app.route("/query", methods=["POST"])
def query():
```
This creates a new Flask route. `query()` function handles user input and returns movie results as JSON.

```
user_input = request.form["query"]
```
This retrieves the form data (i.e, the prompt enetered in the search bar) sent from the browser.\
- `request.form`: dictionary-like object containing form fields.
- `"query"`: name attribute of the <input> in HTML.
- `user_input`: now holds the string typed by the user.

```
mongo_query_text = generate_query(user_input)
```
- Calls the `generate_query` function we defined earlier.
- Sends the `user_input` to Ollama.
- Stores the returned MongoDB query JSON string in `mongo_query_text`.

```
    try:
        mongo_query = json.loads(mongo_query_text)
    except Exception as e:
        print("Model Output:", mongo_query_text)  # DEBUG
        return jsonify({"error": "Model returned invalid JSON"})
```
This is basically a debugging step to handle errors. It tries to convert the string returned by Ollama into a Python dictionary using `json.loads()`. Why? `collection.find()` only works with a Python dict, not a string.\
If parsing fails (AI gave invalid JSON):
- Print the model output to console for debugging.
- Return an error JSON to the browser.

```
    results = list(collection.find(
        mongo_query,
        { "_id": 0, "title": 1 }
    ).limit(20))
```
- Performs a MongoDB query using the dictionary returned by Ollama.
- `collection.find(query, projection)` finds documents matching query.
    - `mongo_query`: dictionary with conditions.
    - `{ "_id": 0, "title": 1 }` → projection: hide _id, only show the title field.
    - `.limit(20)`: returns max 20 results to avoid huge responses.
    - Wrap with `list()`: converts the cursor object into a Python list.

```
    movie_titles = [movie["title"] for movie in results]
```
This ensures only movie titles are extracted and stored in `movie_titles` list. Ex: `["Avatar", "Inception", "Avengers"]`

```
    return jsonify(movie_titles)
```
- Returns the movie titles as a JSON response to the browser.
- Browser JS can then read this and display it in a table, grid, or list.

```
if __name__ == "__main__":
    app.run(debug=True)
```
- This is Python's standard way to run a script only if it’s executed directly (not imported as a module).
- `app.run(debug=True)` starts the Flask dev server.
      - `debug=True` enables hot reload and detailed error messages for development. So that you don't have to restart the server manually again and again after making any changes to `app.py`.\
For folks who work or have worked with **Node.js**, this is like `nodemon` that restarts the node applications when a change in the file is detected.

After you have coded your `index.html` file, you can run your application.

To run your application, type `py app.py` in your VSCode Terminal. You should get: 
```
Running on http://127.0.0.1:5000
```
Hover over the link and click **Follow link** to open the application in your browser.

And that's money!✨ 

If you want to better understand how to make the interface of your web application, You can click on [Understand index.html](03_Understand_index.html.md).\
Need help with your prompts?
[Prompt Guide](04_Prompt_Guide.md).
