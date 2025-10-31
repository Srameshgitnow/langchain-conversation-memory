from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
import getpass
import os
from dotenv import load_dotenv
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")
# Initialize OpenAI LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, openai_api_key=os.environ["OPENAI_API_KEY"])

memory = ConversationBufferMemory(return_messages=True)

conversation = ConversationChain(
    llm=llm,
    memory=memory
)
# prompt template
prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant. Here is the conversation history:
{chat_history}
User: {question}
AI:""")

# chain with memory
chain = (
    RunnableParallel({"chat_history": memory.load_memory_variables, "question": RunnablePassthrough()}) 
    | prompt
    | llm
    | RunnablePassthrough()
)

def chat(question):
    response = chain.invoke({"question": question})
    memory.save_context({"question": question}, {"response": response.content})
    return response.content

# Run the conversation
print("AI:", chat("What is LangChain?"))
print("AI:", chat("How does it use memory?"))
print("AI:", chat("Can you summarize what we talked about?"))

response = conversation.predict(input="What did I just ask?")
print("AI:", response)
