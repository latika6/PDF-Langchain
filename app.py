# create a new environment 
# conda create -p venv python==3.10
# conda activate venv
# google ai studio to get api key
# library to isntall
# streamlit
# google-generativeai
# python-dotenv
# langchain
# PyPDF2
# faiss-cpu
# langchain_google_genai to access the google and gen api
# A vector database is a database that stores, indexes, and queries data as multi-dimensional vectors, also known as vector embeddings:

import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.questions_answering import laod_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
  text = ""
  for pdf in pdf_docs:
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
      text+=page.extract_text()
    return text

# The `RecursiveCharacterTextSplitter` is a tool from LangChain that splits large documents into smaller chunks while preserving context. 
# It uses a hierarchical splitting approach based on delimiters like paragraphs, sentences, and words.
def get_text_chunks(text):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 1000)
  chunks = text_splitter.split_text(text)
  return chunks

# FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering of dense vectors, optimized for large datasets. 
# It is widely used in applications like document retrieval and recommendation systems to find nearest neighbors quickly.
def get_vector_store(text_chunks):
  embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
  vector_store = FAISS.from_text(text_chunks, embedding = embeddings)
  vector_store.save_local("faiss_index")

def get_conversational_chain():
  prompt_template = """
  Answer the question as detailed as possible from provided context, make sure to provide all the details 
  if the answer is not in provided context just say "answer is not available in the context, 
  don't provide the wrong answer
  Context:\n {context}?\n
  Question: \n {question}\n

  Answer:
  """

  model = ChatGoogleGenerativeAI(model = "gemini-pro", temperature=0.3)
  PromptTemplate(template = prompt_template, input_variables = ("context", "question"))
  chain = laod_qa_chain(model, chain_type = "stuff", prompt = prompt)
  return chain

def user_input(user_question):
  embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
  new_db = FAISS.load_local("faiss_index", embeddings)
  docs = new_db.similarity_search(user_question)
  chain = get_conversational_chain()
  
  response = chain(
    {"input_documents":docs, "question":user_question}
    , return_only_outputs = True)

print(response)
st.write("Reply:", response["output_text"])

def main():
  st.set_page_config("Chat with Multiple PDF")
  st.header("Chat with Multiple PDF using Gemini")

  user_question = st.text_input("As question from the PDF file")

  if user_question:
    user_input(user_question)

  with st.sidebar:
    st.title("Menu")
    pdf_docs = st.file_uploader("Uplaod your PDF files and click on the submit and process")
    if st.button("Submit & Process"):
      with st.spinner("Processing..."):
        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        st.success("Done")

if __name__ == "__main__":
  main()


# streamlit run app.py


