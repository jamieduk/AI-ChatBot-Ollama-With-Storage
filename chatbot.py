#!/usr/bin/env python
# coding: utf-8

# In[2]:


from dotenv import load_dotenv
import os 
from langchain_community.llms import Ollama
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough, RunnableParallel


# In[3]:


ollama_llm=Ollama(model='dolphin-llama3:latest') # llama3


# In[4]:


load_dotenv()
API_KEY=os.getenv('OPENAI_API_KEY')
Model='dolphin-llama3:latest' # gpt-3.5-turbo
gpt_llm=ChatOpenAI(api_key=API_KEY,model=Model)


# In[5]:


gpt_llm.invoke('what is a bot')


# In[6]:


parser=StrOutputParser()
gpt_chain=gpt_llm|parser
gpt_chain.invoke('what is a bot')


# In[8]:


loader=TextLoader('data.txt',encoding='utf-8')
document=loader.load()


# In[11]:


spliter=RecursiveCharacterTextSplitter(chunk_size=200,chunk_overlap=50)
chunks=spliter.split_documents(document)
chunks[3]


# In[12]:


vector_storage=FAISS.from_documents(chunks,OpenAIEmbeddings())
retriever=vector_storage.as_retriever()


# In[15]:


retriever.invoke('what is the pricing for Bhuman')


# In[16]:


template=("""
You are AI-powered chatbot designed to provide 
information and assistance for customers
based on the context provided to you only. 
            
Context:{context}
Question:{question}
""")


# In[17]:


prompt=PromptTemplate.from_template(template=template)
prompt.format(
    context=' Here is a context to use',
    question=' This is a question to answer'
)


# In[18]:


result=RunnableParallel(context=retriever,question=RunnablePassthrough())
chain=result |prompt | gpt_llm | parser


# In[19]:


chain.invoke('What is the pricing plan for Bhuman')


# In[20]:


chain.invoke('What is Bhuman')


# In[21]:


chain.invoke('My video is not clear')

