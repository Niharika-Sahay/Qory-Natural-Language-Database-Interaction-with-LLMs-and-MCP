## Installation Guide for Ollama: Gemma 7B
To create your own _Qory_, you would first need to install the brains for it. Gemma 7B is a light-weight open large language model (LLM) created by Google DeepMind which allows you to run AI on consumer-grade hardware, that is your own laptops and desktops. You can learn more about it in the official documentation for [Gemma Models](https://ai.google.dev/gemma/docs).

To install _Gemma_, you'll first need to install [**Ollama**](https://ollama.com/download). Why? Ollama is an open-source tool that simplifies the process of downloading, managing, and running various open-source models. You could think of it as folder consisting of several other AI Model files from where you can install and use not only _Gemma_ but other open-source AI models as well.

Click to install [**Ollama**](https://ollama.com/download) OR [https://ollama.com/download](https://ollama.com/download).

To check if you've installed _Ollama_ properly, open your **Command Prompt** and type: 
```ollama --version``` 
It should show the version you installed: `ollama version is 0.16.3`.
If It Says “ollama is not recognized"; that means Ollama is not installed properly. You should reinstall, and follow the same steps.

After installing _Ollama_, we need to run the _Gemma_ model. To do so, in your Command Prompt type:
```ollama run gemma:7b```
It may take some time to install for the first time.

>[!NOTE]
> If you have less than 8GB RAM and No GPU in your system, install Gemma 7B. Otherwise, Gemma3 12B could be installed if you have available RAM higher than 9.2 GB.
>You can do so by typing `ollama run gemma3:12b`. 

> [!TIP]
> To view your Available RAM do: **Ctrl + Shift + Esc** to open **Task Manager**. Navigate to the **Perfromance** Tab to view **Memory**.

After the download is complete, you'll see:
```>>>```
That means the AI is ready.

Type: `Hello`; if it responds, the Setup is Successful! 🎉

## Other Installations Required
For this project, Python and MongoDB should be installed and set up.

Check if you already have python installed and the path setup: `python --version`.
If not, please follow a tutorial to install and set the path properly. 

Here are quick links to download both Python and MongoDB:
- [Download Python](https://www.python.org/downloads/)
- [Download MongoDB](https://www.mongodb.com/try/download/community)

After all the necessary downloads and setups have been done, we will make the syllabus from where we'll ask questions to our AI aka **DataSet**.
##DataSet Download and Setup
In this project, I have used a Dataset from [Kaggle](https://www.kaggle.com/). It consists two csv files- `tmdb_5000_credits.csv` and `tmdb_5000_movies.csv`. I have used `tmdb_5000_movies.csv`.
To use the same dataset, download it from the link below. It'll be downloaded as a zip file. Extract all.
Click to [Download Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
Then open **MongoDB compass**. Connect to your `localhost` connection. Then create a _Database_ named **Movies** or any name of your choice. Inside the database, create a _Collection_ named **movie_dataset** or again, any name of you choice.
Open the Collection and click on **Import Data**, then import `tmdb_5000_movies.csv`. You can also remove any fields you do not want to use by simply unchecking the column. You can also change the datatypes of the fields through the drop down that appears beside them.
Here's how I had structured the documents in my Collection: 
```
_id: ObjectId\(699b2217d853bddf30992016\)
genres:Array (4)
keywords:Array (21)
original_language:"en"
original_title:"Avatar"
overview:"In the 22nd century, a paraplegic Marine is dispatched to the moon Pan…"
production_companies:Array (4)
runtime:162
tagline:"Enter the World of Pandora."
title:"Avatar"
vote_average:7.2
vote_count:11800
```
As you may notice, I have deleted some fields that I did not require. This allows the dataset to be clear and easier for our Model to search through.

Finishing this step, brings you to the final step of setups required for creating your AI bud.

##Setting up the Environment 
-Now, create a folder and name your project. I'll be naming mine as **AI_Search** for this documentation.
-Open the folder in _VSCode_.
-Open your Terminal in VSCode. Create a Virtual Environment:
```py -3 -m venv .venv```
-Activate the Virtual Environment:
```.venv\Scripts\activate```
-Then type:
```pip install flask pymongo requests``` 
This installs three essential Python Libraries: **Flask** creates a web server, **PyMongo** enables communication with a MongoDB database, and **Requests** allows your application to send HTTP requests to other web services.
-Then you should write your code. And to run your app.py, run the following command in your Terminal:
```py app.py```

Wohoo!🎉 Now, you are absolutely ready to Create your own AI friend 😎. If you want to understand the code and be able to implement this project in your own style, visit:
[Understand app.py](docs/Understand_app.py.md)
[Understand index.html](docs/Understand_app.py.md)
Need help with Prompts?
[Prompt Guide](docs/Prompt_Guide.md)

