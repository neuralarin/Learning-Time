from dotenv import load_dotenv 
from langchain_mistralai import ChatMistralAI 
from langchain.messages import HumanMessage, AIMessage, SystemMessage 

load_dotenv() 

model = ChatMistralAI(model="mistral-small-2603", temperature=0.9, max_tokens=40) 

print("----------Hi, I am Aura type # to exit the application----------")

print("Choose your AI mode")
print("Press 1 for funny mode")
print("Press 2 for emotional mode")
print("Press 3 for angry mode")

choice = (int(input("Choose your mode: ")))

if choice == 1:
    mode = "You are a funny AI agent. You crack concepts in joke"
elif choice == 2:
    mode = "You are a emotional AI agent. You gets emotional while explaining concepts"
elif choice == 3:
    mode = "You are a agressive AI agent. You respond aggresively and impatiently"


messages = [ SystemMessage(content=mode) ] 


while True: 
    prompt = input("You: ") 

    messages.append(HumanMessage(content=prompt)) 
    if prompt == "#": 
        break

    response = model.invoke(messages) 
    messages.append(AIMessage(content=response.content)) 
    print("AI:", response.content)