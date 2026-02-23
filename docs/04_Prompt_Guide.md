## Everything you need to know about Prompts

While you begin to work on a project like this, related to AI Integrations, there might be so many spiraling questions. And while you can go ahead and always ask ChatGPT, you being redirected to this documentation has to be a sign 🎱! So, it is upon me to bestow all my knowledge upon you that I gathered while working on this project.\
Let's dive right in!

## Why do we need Prompts?
We need them to bridge the gap between human intent and AI output; ensuring the model delivers accurate, relevant, and high-quality results.\
In our case, it is to convert natural language movie search queries into valid MongoDB filter objects.\
Ex: Instead of writing database queries manually, users can type:\
_"Action movies above rating 8"_\
And our AI can convert it into `{ "genres.name": "Action", "vote_average": { "$gt": 8 } }`. This filter can then be executed directly on the MongoDB collection.

Now, if you are brilliant like me, you might have a question. "When we are writing the propmt to Gemma in `app.py`, how are we training Gemma? And then on the webpage when we search in the search bar, that is also `user_propmt`, how is that different?"

Q1\) How is the prompt mentioned in `app.py` training Gemma?\
Ans: We are not training Gemma, we are just providing it constraints so that it gives as correct of a response as it can.\
Gemma Is Already Pretrained. Gemma:7B is a large language model \(LLM\) that has been trained on massive amounts of text: books, code, web pages, tutorials, and documentation. During its pretraining, it learned patterns in language, reasoning, and code-like structures, including JSON, MongoDB queries, SQL, etc. We do **NOT** train it further for this project. What we do is prompt it correctly.

When we write:
```
You are a MongoDB query generator.
Return ONLY valid JSON.
Schema: genres.name, vote_average, runtime
Input: Action movies
Output: { "genres.name": "Action" }
User Query: Movies above rating 8
```
We are essentially setting up these following parameters:
- **Role instruction**: “You are a MongoDB query generator”
  Tells the model: “Focus on generating queries, not explanations.”
- **Constraints on datatypes**: “Return only JSON, no backticks, no extra text”
  Avoids messy output.
- **Schema**: Tells it what fields exist in the database.
- **Examples** → “Show me examples of input → output”
  This is called few-shot prompting. The model sees patterns and learns from them in context.
  `Input: Action movies. Output: { "genres.name": "Action" }`
- **User Query**: This is the actual input we want it to process.

So, in a way, we are “training” it **in-context**, not by updating weights, but by showing examples and instructions.\
It's like asking ChatGPT: "You are a my Professor. Ask me viva questions related to VLSI Design, MOSFETS & IRDS Roadmap". Note how we can change the roles for ChatGPT depending on the situation. In our project, we have only one dataset and only one goal, i.e, to display movie titles based on filters applied by the user. In such a case, it is only smart to set the above constraints so that Gemma filters out movies as precisely as possible. 

Q2\) How is the `user_prompt` different from the **"pre-specified prompt"**?\
Ans: The `user_prompt` is what we are required to extract from the databse. Whereas, the pre-specified prompt only helps to extract those fields more precisely and avoid hallucinations and incorrect datatype returns.

Then you may also be interested in knowing what is **Local AI** and how does it work on your laptops and desktops?

### Difference between Gemma & ChatGPT
To understand the difference between a Local AI and one that is run on the Cloud, you'll need to understand what a local server is.\
Firstly, a “server” is basically any program that waits for requests and sends responses. Your computer is now acting like a server.\
In this case:
- Flask → your Python app server (listens for browser requests, serves pages)
- Ollama Gemma → the AI server (listens for API calls, returns query JSON)\
So even though it’s called a “server,” it’s just software running on your laptop that other software \(Flask\) can talk to.

### How Gemma Works Locally
When you run: `ollama serve`
- Ollama starts a local API server on your computer.
- Port 11434 (or another port) is like the “door” your Python code uses to talk to Gemma.
- `gemma:7b` model loads into your RAM + GPU (if available).
```
User types query → Flask → POST request → Ollama local server → Gemma model → JSON output → Flask → browser
```

## Model Information
Even though I have mentioned it multiple times throughout all documentation, below is the Model Information used for this project:\
- **Model**: gemma:7b
- **Runtime**: Local (via Ollama)
- **Fine-tuning**: None
- **Approach**: Prompt Engineering + Few-Shot Learning
The important thing to understand is that this model is not trained specifically for this task, i.e, _Extracting Movie Titles from a Database_.\
It relies on its pre-trained language understanding and pattern recognition abilities. And the behavior is shaped entirely through structured prompting which we have talked about earlier in this documentation.

## Database Schema Constraints
To reduce hallucinations and invalid queries, we have restricted the model to the following fields:
- `genres.name`
- `keywords.name`
- `vote_average`
- `runtime`
- `original_language`\
The prompt explicitly lists these fields to guide output generation.\
This ensures:
- No unexpected keys
- No invented fields
- Cleaner JSON parsing

## Prompt Structure Breakdown
Even though we have talked about the Propmpt Structure breifly above in this documentation, here's a detailed version of it. 

- **Role Definition**
  ```
  You are a MongoDB query generator.
  ```
  This anchors the model to a strict functional role instead of a conversational one.

  - **Output Constraints**
    ```
    Do not explain anything.
    Do not add backticks.
    Do not add text before or after JSON.
    ```
    These constraints are critical because:
    - LLMs tend to add explanations.
    - LLMs often wrap JSON in markdown blocks.
    - Any extra text breaks json.loads().
    - This forces structured output.
  
  - **Schema Declaration**
    ```
    -genres.name
    -keywords.name
    -vote_average
    -runtime
    -original_language
    ```
    This reduces hallucination by explicitly restricting usable fields.

  - **Few-Shot Examples**
    ```
    Input: Action movies
    Output: { "genres.name": "Action" }

    Input: Movies above rating 8
    Output: { "vote_average": { "$gt": 8 } }
    ```
    This is called **few-shot prompting**.\
    Instead of retraining the model, we show it:
      - The expected input format
      - The expected output format
      - The correct MongoDB syntax pattern
      - The model then mimics the structure for new queries.

  ## How Gemma Converts Language to MongoDB Queries
  Gemma does not "understand MongoDB" like a database engine.\
  Instead, it:
     - Recognizes patterns in natural language.
     - Maps phrases to structured logic.
  Examples:
| Natural Language        | MongoDB Equivalent          |
| ----------------------- | --------------------------- |
| above rating 8          | `$gt: 8`                    |
| below rating 5          | `$lt: 5`                    |
| Action movies           | `"genres.name": "Action"`   |
| longer than 150 minutes | `"runtime": { "$gt": 150 }` |
It predicts the most statistically likely structured JSON output based on training data patterns.\
This is probabilistic pattern matching — not rule-based parsing.

## Output Cleaning
LLMs often return JSON wrapped in markdown like: `{ "vote_average": { "$gt": 8 } }`\
To prevent parsing errors, the backend cleans the output:
```
result = result.replace("```json", "")
result = result.replace("```", "")
result = result.strip()
```
This ensures the string is pure JSON before calling: `json.loads(mongo_query_text)`

## Limitations
This system has practical constraints:
- Language filtering may not always work reliably.
- Very Complex multi-condition queries may fail.
- No semantic ranking (results are exact filter matches).
- No fuzzy search.
- The system prioritizes simplicity and local execution over advanced ranking logic.

## Example Test Queries
And as you reach closer to creating your own AI Explorer, here are some `user_prompts` you can try to test your application:
- Action movies above rating 7
- Movies longer than 150 minutes
- Science Fiction movies
- Comedy movies under rating 6
- Movies above rating 8 and runtime above 120
- Movies in English

## Why Prompt Engineering Instead of Fine-Tuning?
As we are running entirely on local hardware,\
Fine-tuning:
- Requires larger compute resources
- Requires dataset preparation
- Increases model size
Prompt engineering was chosen because:
- It works efficiently on limited hardware
- It keeps the system lightweight
- It avoids retraining costs

This makes _Qory_ practical and portable✨

Other Quick Links for Navigation:
- [Get Quick Overview of the Project](README.md)
- [Installation & Setup](docs/01_Installation_&_Setup.md)
- [Understand app.y](docs/02_Understand_app.py.md)
- [Understand index.html](docs/03_Understand_index.html.md)


