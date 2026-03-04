from langchain_openai import AzureChatOpenAI  
from dotenv import load_dotenv

load_dotenv()
MODEL_DEPLOYMENT_NAME='gpt-4.1'

llm = AzureChatOpenAI(azure_deployment=MODEL_DEPLOYMENT_NAME)
answer = llm.invoke('why python is the most popular language?') 
print(answer)

llm = AzureChatOpenAI(
          deployment_name=MODEL_DEPLOYMENT_NAME, 
          temperature=0
      ) 

answer = llm.invoke('why python is the most popular language? answer the Korean') 
print(answer.content)