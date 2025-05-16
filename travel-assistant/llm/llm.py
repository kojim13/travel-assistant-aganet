import os

#from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

# def get_model() -> ChatGoogleGenerativeAI:
#     model_name = os.getenv("LLM_MODEL", "gemini-1.5-flash")
#     return ChatGoogleGenerativeAI(model=model_name)

def get_model() -> OllamaLLM:
    model_name = os.getenv("LLM_MODEL", "llama3")
    return OllamaLLM(model=model_name)

