from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain.agents import create_agent

############# AI tools #################


@tool
def get_account_balance() -> float:
    """Get the current account balance for the authenticated user."""
    return 1250.75


############# Utils #################
def print_agent_conversation(messages):
    for message in messages:
        print(type(message).__name__)
        print(message.content.strip())
        print("---")


############# Main code #################
llm = ChatOllama(
    model="llama3.2:1b"
)


agent = create_agent(
    model=llm,
    tools=[get_account_balance],
)

messages = [
    SystemMessage(content="""
        You are a helpful bank AI assistant.Be concise and never invent account information.
    """)]

messages.append(
    HumanMessage(content="""
        Get my current balance
    """)
)

result = agent.invoke({"messages": messages})


# Only invoke this when the file is executed directly, such as running python main.py
if __name__ == "__main__":
    print_agent_conversation(result["messages"])


def manual_tool_call():
    messages = [
        SystemMessage(
            content="You are a helpful bank AI assistant. "
                    "Be concise and never invent account information."
        )
    ]

    llm_with_tools = llm.bind_tools(
        [get_account_balance]
    )

    # messages.append(
    #     HumanMessage(content="My name is Ahmed.")
    # )

    # response = llm_with_tools.invoke(messages)

    # print("Assistant:", response.content)

    # # Add the assistant's response to the conversation
    # messages.append(response)

    # # Second turn
    # messages.append(
    #     HumanMessage(content="What is my name?")
    # )

    # response = llm_with_tools.invoke(messages)

    # print("Assistant:", response.content)

    # messages.append(
    #     HumanMessage(content="Ge my current account balance?")
    # )

    # response = llm_with_tools.invoke(messages)

    # print(response.tool_calls)

    messages.append(
        HumanMessage(content="Get my current account balance?")
    )

    response = llm_with_tools.invoke(messages)

    print("Content:", response.content)
    print("Tool calls:", response.tool_calls)

    if response.tool_calls:
        tool_call = response.tool_calls[0]

        tool_result = get_account_balance.invoke(
            tool_call["args"]
        )

        messages.append(response)

        # Wrap tool result in a ToolMessage since, messagaes only accept LangChain message objects
        # Without this step it will throw an exception, since you're trying to append float value in a list of LangChain message objects
        messages.append(
            ToolMessage(content=str(tool_result),
                        tool_call_id=tool_call["id"],)
        )

        final_response = llm_with_tools.invoke(messages)

        print("Assistant:", final_response.content)
