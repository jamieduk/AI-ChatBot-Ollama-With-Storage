#!/usr/bin/env python
# coding: utf-8

from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

# Load environment variables
load_dotenv()

# Initialize Ollama local language model
print("Initializing Ollama local language model...")
ollama_llm=Ollama(model='dolphin-llama3:latest') # llama3
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


# Set up runnable process
result=RunnableParallel(context=RunnablePassthrough(), question=RunnablePassthrough())
chain=result | prompt | ollama_llm | StrOutputParser()

# Invoke the chain with the user's input
print("Invoking the chain with the user's input...")
output=chain.invoke(question)
print("Chain invoked.")
print("Output:", output)

