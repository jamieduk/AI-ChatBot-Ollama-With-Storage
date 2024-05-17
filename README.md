# AI-ChatBot-Ollama-With-Storage

## Introduction
This AI Bot is designed to answer user questions using the Ollama local language model. It checks if the question has been asked before and retrieves the answer if available in the data file. Otherwise, it invokes the Ollama model to provide an answer and stores it for future use.

## Setup

### Windows

1. Create a virtual environment:
    ```
    venv
    ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run the bot using `start.bat`:
    ```
    start.bat
    ```

### Linux

1. Create a virtual environment:
    ```
    venv
    ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run the bot using `./start.sh`:
    ```
    ./start.sh
    ```

## Files
- `chatbot.py`: Main Python script.
- `requirements.txt`: List of Python dependencies.
- `start.bat`: Windows batch script to start the bot.
- `run.bat`: Windows batch script to run the bot continuously.
- `start.sh`: Linux shell script to start the bot.
- `output.txt`: File to store question-answer pairs.
- `embeddings.txt`: File to store question-answer embeddings.

## Usage
1. Run the bot according to the setup instructions for your operating system.
2. Enter the context (leave blank for default) and your question when prompted.
3. The bot will check if the question has been asked before.
4. If the answer exists in the data file, it will be displayed.
5. If not, the bot will invoke the Ollama model to answer the question.
6. The result will be stored in `output.txt` and `embeddings.txt`.
7. The final response will be displayed.

## Notes
- Ensure proper configuration of environment variables and the Ollama model in `.env`.
- Customize error handling and logging as per requirements.
