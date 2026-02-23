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
To learn how to setup your Dataset click: 
