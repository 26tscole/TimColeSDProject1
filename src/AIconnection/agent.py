import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.AIconnection.userTools import getCurrentDatetime, getAvailableMeetings, getBookings


max_iterations = 5
def buildAIFunctionality():
    tools = [getCurrentDatetime, getAvailableMeetings, getBookings]
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        api_key=os.environ.get("GEMINI_API_KEY")
    )
    llm = llm.bind_tools(tools)
    return llm

def sendAIrequest(llm, userInput):

    system_message = SystemMessage(
        content="You are an ai agent that will search through api data and respond "
                "to the user about open reservations and currently booked reservations."
                "Use the least amount of tools as possible"
                "Return your response in json format with two keys:\n"
                "1. 'message': A brief explanation of what you found\n"
                "2. 'data': The list of items from the tool result\n"
                "Example: {'message': 'Found 3 bookings', 'data': [...]}"
                "If no data found return"
                "1. 'message': What you couldn't find\n"
                "2. 'data': Empty list\n"
)
    user_message = HumanMessage(content=userInput)
    messages = [system_message, user_message]

    tools = [getCurrentDatetime, getAvailableMeetings, getBookings]
    llmWithTools = llm.bind_tools(tools)

    tool_map = {
        'getCurrentDatetime': getCurrentDatetime,
        'getAvailableMeetings': getAvailableMeetings,
        'getBookings': getBookings
    }

    # Wanted to make sure there isn't infinite calling of tools which would cause massive issues I believe
    for _ in range(max_iterations):
        response = llmWithTools.invoke(messages)

        if not response.tool_calls:
            formattedResponse(response.content)
            return

        messages.append(response)

        for tool_call in response.tool_calls:
            result = tool_map[tool_call['name']].invoke(tool_call['args'])
            messages.append(HumanMessage(content=str(result), tool_call_id=tool_call['id']))

    print("Max iterations reached.")

def formattedResponse(response):
    try:
        parsedResponse = json.loads(response[0]["text"])
        print("AI RESPONSE:\n")
        for key, value in parsedResponse.items():
            if key == "message":
                print(
                    "-"*len(value),"\n",
                    value,"\n",
                    "-" * len(value),"\n"
                )
            elif key == "data":
                if not value:
                    print("No data found")
                    return
                for item in value:
                    print(item)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON error: {e}")
        print(f"Content was: {response}")
        return None
