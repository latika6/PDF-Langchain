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
# langchaib_google_genai to access the google and gen api

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
from dotenv import laod_dotenv



