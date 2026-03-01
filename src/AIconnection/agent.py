import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.setEnviron import loadSecrets
from src.meetIngActions.users import Users


if __name__ == "__main__":
    loadSecrets()
    user = Users()

    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        api_key=os.environ.get("GEMINI_API_KEY")
    )

    # System message - defines what the agent does
    system_message = SystemMessage(
        content="You are an ai agent that will search through api data and respond "
                "to the user about open reservations and currently booked reservations."
    )

    # User message - the actual request
    user_message = HumanMessage(
        content="What kind of agent are you"
    )

    response = llm.invoke([system_message, user_message])
    text = response.content[0].get("text")
    print(text)
