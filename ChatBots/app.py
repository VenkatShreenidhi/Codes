import streamlit as st 
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser 
from langchain_core.prompts.chat import ChatPromptTemplate
import os 

from dotenv import load_dotenv 

load_dotenv()


os.environ["OPENAI_API_KEY"]= os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"]= os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]= "True"


#st.write(os.environ["OPENAI_API_KEY"])
#st.write(os.getenv("OPENAI_API_KEY")) 

## PROMPTS 

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a Q&A bot, Whatever is question is asked kindly provide relevant and resource back answer "),
        ("user","Question:{question}")

    ]
)

def give_answer(question,api_key,llm,temperature,max_tokens):
    openai.api_key=api_key
    llm =ChatOpenAI(model=llm)
    outputParse = StrOutputParser()
    chain = prompt|llm|outputParse
    answer = chain.invoke({'question':question})
    return answer


# streamlit 

st.title("Q&A BOT")

st.sidebar.title("Get Model, Temperature, Max_tokens details")
api_key = st.sidebar.text_input("Enter the OPEN AI API KEY ", type="password")

llm = st.sidebar.selectbox("Select an Open AI model", ["gpt-4","gpt-4o-mini","gpt-3.5-turbo" ])

temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0)
max_tokens = st.sidebar.slider("Max_tokens", min_value=50, max_value=200)


# main 

st.write("Ask a question about anything")
user_input = st.text_input("You:")

if user_input:
    response = give_answer(user_input,api_key,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")