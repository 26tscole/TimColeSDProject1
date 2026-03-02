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
        content="You are an AI agent that searches API data for reservations."
                "PROCESS:"
                "1. Call the appropriate tool ONCE to get data"
                "2. You can call multiple tools if the user asks a question that requires more than one tool"
                "2. IMMEDIATELY return a JSON response - DO NOT call tools again"
                "RESPONSE FORMAT (required):"
                "{message: Give the user a brief response that has to do with their question, data: [list of items]}"
                "Examples:"
                "- Found data: {message: Give the user a brief response that has to do with their question, data: [...]}"
                "- No data: {message: Give the user a brief response that has to do with their question, data: []}"
                "DO NOT call the same tool twice."
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
    for iteration in range(max_iterations):
        response = llmWithTools.invoke(messages)

        print(f"\n=== Iteration {iteration + 1} ===")
        print(f"Has tool calls: {bool(response.tool_calls)}")
        print(f"Number of tool calls: {len(response.tool_calls) if response.tool_calls else 0}")

        if not response.tool_calls:
            print("No tool calls - sending to formattedResponse")
            formattedRooms(response.content)
            return

        messages.append(response)

        for tool_call in response.tool_calls:
            print(f"Calling: {tool_call['name']} with args: {tool_call['args']}")
            result = tool_map[tool_call['name']].invoke(tool_call['args'])
            print(f"Tool result: {result}")
            messages.append(HumanMessage(content=str(result), tool_call_id=tool_call['id']))

    print("\n!!! Max iterations reached - LLM never stopped calling tools !!!")

    print("Max iterations reached.")

def formattedRooms(response):
    try:
        print (response)
        # We cannot have single quotes so this was my solution
        if isinstance(response, list) and len(response) > 0:
            response = response[0].get('text', '')
            print(response)
        response = response.replace("'", '"')
        parsedResponse = json.loads(response)
        print("AI RESPONSE:\n")
        for key, value in parsedResponse.items():
            if key == "message":
                print("-" * len(value))
                print(value)
                print("-" * len(value))

            elif key == "data":
                if not value:
                    return
                for i, item in enumerate(value, 1):
                    print(f"\nItem {i}:")
                    for itemKey, itemValue in item.items():
                        if isinstance(itemValue, dict):
                            print(f"  {itemKey}:")
                            for nestedKey, nestedValue in itemValue.items():
                                print(f"    {nestedKey}: {nestedValue}")
                        else:
                            print(f"  {itemKey}: {itemValue}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON error: {e}")
        print(f"Content was: {response}")
        return
