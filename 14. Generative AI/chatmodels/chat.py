from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

model = ChatMistralAI(model="mistral-small-2603", temperature=0.9, max_tokens=40)

messages = [
    SystemMessage(content="You are a funny AI agent")
]

print("----------Welcome type # to exit the application----------")

while True:
    
    prompt = input("You: ")
    messages.append(HumanMessage(content=prompt))
    if prompt == "#":
        break
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print("AI:", response.content)