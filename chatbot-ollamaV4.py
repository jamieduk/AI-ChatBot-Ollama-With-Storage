
# https://github.com/jamieduk/AI-ChatBot-Ollama-With-Storage
import os
import time
import re
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

def format_duration(duration):
    hours=duration // 3600
    minutes=(duration % 3600) // 60
    seconds=duration % 60

    if hours > 0:
        return f"{int(hours)} hour{'s' if hours > 1 else ''}, {int(minutes)} minute{'s' if minutes > 1 else ''}, {seconds:.2f} seconds"
    elif minutes > 0:
        return f"{int(minutes)} minute{'s' if minutes > 1 else ''}, {seconds:.2f} seconds"
    else:
        return f"{seconds:.2f} seconds"

def store_embeddings(question, answer, filename="output.txt"):
    # Store question and answer embeddings in the specified file
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"Q: {question}\nA: {answer}\n")

def find_answer_in_data(question, filename="output.txt"):
    # Check if the question has been asked before by searching in the specified file
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            lines=f.readlines()
            for i in range(0, len(lines), 2):
                if lines[i].strip() == f"Q: {question}":
                    return lines[i + 1].strip().replace("A: ", "")
    return None

# Initialize Ollama local language model
print("Initializing Ollama local language model...")
try:
    ollama_llm=Ollama(model='dolphin-llama3:latest')  # Adjust the model name as needed
    print("Ollama local language model initialized.")
except Exception as e:
    print(f"Failed to initialize Ollama local language model: {e}")
    exit(1)

# Get user input
context=input("Enter the context (leave blank for default): ")
question=input("Enter your question: ")

# Check if the question has been asked before
print("Checking if the question exists in data file...")
answer=find_answer_in_data(question)

if answer:
    print("Answer found in data file:", answer)
else:
    # Combine context and question into a single input string
    input_text=f"Context: {context}\nQuestion: {question}"
    print("No answer found in data file.")
    print("Combined input text:", input_text)

    # Invoke the chain with the user's input and measure the duration
    print("Invoking the chain with the user's input...")
    start_time=time.time()  # Record start time
    try:
        # Debugging print statement before invoking
        print("Before invoking Ollama model")

        # Simplified test for invoking the model
        chain_output=ollama_llm.invoke(input=input_text)

        # Debugging print statement after invoking
        print("After invoking Ollama model")

        end_time=time.time()  # Record end time
        duration=end_time - start_time  # Calculate duration

        if not chain_output:
            print("Chain invocation returned no output.")
        else:
            print("Chain invoked successfully.")
            print("Raw output from chain:", chain_output)

    except Exception as e:
        print(f"Failed to invoke the chain: {e}")
        exit(1)

    # Format and print the duration
    print("Query took", format_duration(duration))

    # If there is valid output, store it in the output.txt file and embeddings.txt file
    if chain_output:
        print("Storing the result in output.txt")
        store_embeddings(question, chain_output, "output.txt")
        print("Storing the result in embeddings.txt")
        store_embeddings(question, chain_output, "embeddings.txt")

    # Strip non-alphanumeric characters from output for final response
    alphanumeric_output=re.sub(r'\W+', ' ', chain_output)
    print("Final Response:", alphanumeric_output)

