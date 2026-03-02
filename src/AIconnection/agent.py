import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.AIconnection.userTools import (
    getCurrentDatetime,
    getAvailableMeetings,
    getBookings,
    setUsersInstance,
)
from src.setEnviron import loadSecrets
from src.meetIngActions.users import Users
from src.conversion.SpeechToText import audioSource


# this function will return the specific data from the AI response
def runAIChat(source="microphone", audioFilePath=""):
    responses = []
    print("To send AI request say 'Send Message'")
    print("To end chat with AI say 'Stop Chat'")
    while True:
        audioSource(txtFileName="AIFile", source=source, audioFilePath=audioFilePath)
        loadSecrets()
        user = Users()
        llm = buildAIFunctionality()
        setUsersInstance(user)
        with open("AIFile", "r") as f:
            content = f.read()
        content = content.lower()
        content = content.replace("send message", "")
        if "stop chat" in content:
            print("GoodBye!")
            break
        if "reset" in content:
            print("Reset!")
            continue
        responses.append(sendAIrequest(llm=llm, userInput=content))
        if source == "file":
            break
    return responses


def buildAIFunctionality():
    tools = [getCurrentDatetime, getAvailableMeetings, getBookings]
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest", api_key=os.environ.get("GEMINI_API_KEY")
    )
    llm = llm.bind_tools(tools)
    return llm


def sendAIrequest(llm, userInput):

    system_message = SystemMessage(
        content="You are an AI agent that searches API data for reservations."
        "PROCESS:"
        "1. Call the appropriate tool ONCE to get data"
        "2. You can call multiple tools if the user asks a question that requires more than one tool"
        "2. IMMEDIATELY return a VALID JSON response. Use double quotes for ALL keys and values."
        "RESPONSE FORMAT (required):"
        '"{message": "Give the user a brief response that has to do with their question", '
        '"data": [list of items]}'
        "Examples:"
        "- Found data: "
        '{"message": "Give the user a brief response that has to do with their question", '
        '"data": [...]}'
        "- No data: "
        '{"message": "Give the user a brief response that has to do with their question", '
        '"data": []}'
        "DO NOT call the same tool twice."
        "DO NOT call a tool if the request doesn't need a tool to be answered"
    )

    user_message = HumanMessage(content=userInput)
    messages = [system_message, user_message]

    tools = [getCurrentDatetime, getAvailableMeetings, getBookings]
    llmWithTools = llm.bind_tools(tools)

    tool_map = {
        "getCurrentDatetime": getCurrentDatetime,
        "getAvailableMeetings": getAvailableMeetings,
        "getBookings": getBookings,
    }

    # Wanted to make sure there isn't infinite calling of tools which would cause massive issues I believe
    max_iterations = 5
    for iteration in range(max_iterations):
        response = llmWithTools.invoke(messages)

        print(f"\n=== Iteration {iteration + 1} ===")
        print(f"Has tool calls: {bool(response.tool_calls)}")
        print(
            f"Number of tool calls: {len(response.tool_calls) if response.tool_calls else 0}"
        )

        if not response.tool_calls:
            print("No tool calls - sending to formattedResponse")
            return formattedRooms(response.content)

        messages.append(response)

        for tool_call in response.tool_calls:
            print(f"Calling: {tool_call['name']} with args: {tool_call['args']}")
            result = tool_map[tool_call["name"]].invoke(tool_call["args"])
            print(f"Tool result: {result}")
            messages.append(
                HumanMessage(content=str(result), tool_call_id=tool_call["id"])
            )

    print("\n!!! Max iterations reached - LLM never stopped calling tools !!!")
    print("Max iterations reached.")
    return None


def parseResponse(response):
    if isinstance(response, list) and len(response) > 0:
        response = response[0].get("text", "")
    parsedResponse = json.loads(response)
    return parsedResponse


def printMessage(value):
    print("-" * len(value))
    print(value)
    print("-" * len(value))


def printItem(value):
    for i, item in enumerate(value, 1):
        print(f"\nItem {i}:")
        for itemKey, itemValue in item.items():
            if isinstance(itemValue, dict):
                print(f"  {itemKey}:")
                for nestedKey, nestedValue in itemValue.items():
                    print(f"    {nestedKey}: {nestedValue}")
            else:
                print(f"  {itemKey}: {itemValue}")


def formattedRooms(response):
    try:
        parsedResponse = parseResponse(response)
        print("AI RESPONSE:\n")
        for key, value in parsedResponse.items():
            if key == "message":
                printMessage(value)
                continue
            if not value:
                return None
            printItem(value)
        return parsedResponse
    except json.JSONDecodeError as e:
        print(f"Invalid JSON error: {e}")
        print(f"Content was: {response}")
        return None
