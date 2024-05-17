#!/usr/bin/env python
# coding: utf-8

import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_community.document_loaders import TextLoader
import time

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

# Initialize Ollama local language model
print("Initializing Ollama local language model...")
ollama_llm=Ollama(model='dolphin-llama3:latest')  # llama3
print("Ollama local language model initialized.")

# Define prompt template
default_context="No specific context provided."
template=("""
You are an AI-powered chatbot designed to provide 
information and assistance for customers
based on the context provided to you only. 
            
Context:{context}
Question:{question}
""")

# Format prompt template
context=input("Enter the context (leave blank for default): ")
if not context:
    context=default_context

question=input("Enter your question: ")
prompt=PromptTemplate.from_template(template=template)
prompt.format(
    context=context,
    question=question
)

# Load data from text file
text_file="data.txt"
if os.path.isfile(text_file):
    loader=TextLoader(text_file, encoding='utf-8')
    document=loader.load()
else:
    document=""

# Set up runnable process
result=RunnableParallel(context=RunnablePassthrough(), question=RunnablePassthrough())
chain=result | prompt | ollama_llm | StrOutputParser()

# Invoke the chain with the user's input and measure the duration
print("Invoking the chain with the user's input...")
start_time=time.time()  # Record start time
output=None
try:
    output=chain.invoke(question)
except Exception as e:
    print("An error occurred while invoking the chain:", e)

end_time=time.time()  # Record end time
duration=end_time - start_time  # Calculate duration

print("Chain invoked.")
print("Output:", output)
# Format and print the duration
print("Query took", format_duration(duration))

# If there is valid output, store it in the output.txt file
if output:
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(output)

# If there are no valid text chunks found in the document, skip processing embeddings
if document:
    # Split text into chunks
    spliter=RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    chunks=spliter.split_documents(document)

    # Generate embeddings for text chunks only if there are chunks available
    if chunks:
        # Generate embeddings for text chunks
        embeddings=OpenAIEmbeddings()

        # Create vector storage from text chunks
        vector_storage=FAISS.from_documents(chunks, embeddings)

        # Retrieve embeddings for each chunk and append them to the data.txt file
        with open("data.txt", "a", encoding="utf-8") as f:
            for chunk in chunks:
                try:
                    embeddings=embeddings.generate(chunk)
                    embeddings_str=" ".join(map(str, embeddings))
                    f.write(embeddings_str + "\n")
                except Exception as e:
                    print("An error occurred while generating embeddings:", e)
                    continue

        print("Embeddings stored in data.txt")
    else:
        print("No valid text chunks found in the document.")

