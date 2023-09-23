import os
import streamlit as st
import langchain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import pickle
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQAWithSourcesChain

from dotenv import load_dotenv
load_dotenv()

st.title('AI Chatbot')
with st.sidebar.title('Get Information about the courses'):
    st.subheader('''
                Brainlox offers high level technical courses.
                To know about all courses,talk to our chatbot.
                ''')
    
# load the csv file
loader=CSVLoader('scraped_data.csv',encoding='utf-8')
data=loader.load()

# remove the '\n' at the end of the URLs
for item in data:
    if 'Course URL' in item:
        item['Course URL']=item['Course URL'].strip()

# Split the text into chunks
splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
chunks=splitter.split_documents(data)

# Get word embeddings and use FAISS for similarity search for word embeddings
if os.path.exists('courseData.pkl'):
    with open('courseData.pkl','rb') as f:
        vectorstore=pickle.load(f)
else:
    embeddings=OpenAIEmbeddings()
    vectorstore=FAISS.from_documents(chunks,embedding=embeddings)
    with open('courseData.pkl','wb') as f:                      
        pickle.dump(vectorstore,f)

# Initialize LLM
llm=OpenAI(temperature=0, max_tokens=500)
chain = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())
# langchain.debug=True

# User input
query=st.text_input('Write your question here')
if query:
    llm=OpenAI(temperature=0, max_tokens=500)
    chain = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())
    result=chain({"question": query}, return_only_outputs=True)
    st.header("Answer")
    st.subheader(result['answer'])