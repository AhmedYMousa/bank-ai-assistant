from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.prebuilt import ToolRuntime
from pydantic import BaseModel
from models import Transaction, AccountBalance, TransactionResult, TransactionServiceError,  UserContext

############# Utils #################


def print_agent_conversation(messages):
    for message in messages:
        print(type(message).__name__)
        print(message)
        # print(message.content.strip())
        print("---")


def _get_recent_transactions(user: UserContext) -> list[Transaction]:
    # raise TransactionServiceError(
    #     "Transaction service is currently unavailable."
    # )
    print(f"Loading transactions for {user.user_id}")

    return [
        Transaction(
            date="2026-09-15",
            description="Supermarket",
            amount=-45.0,
        ),
        Transaction(
            date="2026-09-14",
            description="Salary",
            amount=2500.00,
        ),
        Transaction(
            date="2026-09-13",
            description="Coffee Shop",
            amount=-5.00,
        ),
    ]


############# AI tools #################
@tool
def get_account_balance() -> AccountBalance:
    """Get the current account balance for the authenticated user."""
    return AccountBalance(amount=1250.75, currency="USD")


@tool
def get_recent_transactions(runtime: ToolRuntime[UserContext],) -> TransactionResult:
    """Get the recent transactions for the authenticated user.

    Use this tool when the user wants to see, inspect, or discuss
    individual transactions.
    """

    try:
        return TransactionResult(transactions=_get_recent_transactions(runtime.context))

    except TransactionServiceError as error:
        return TransactionResult(
            error="TRANSACTION_SERVICE_UNAVAILABLE",
            message=str(error))


@tool
def calc_net_transactions(runtime: ToolRuntime[UserContext]) -> dict:
    """Calculate the net transaction amount from the user's recent transactions.

    Use this tool when the user asks for the net, total, or combined
    amount of their transactions. Do not calculate the amount yourself.
    """
    try:
        transactions = _get_recent_transactions(runtime.context)
        # We've changed the response into pushing deterministic semantics into deterministic code
        return {
            "type": "net_transaction_amount",
            "currency": "USD",
            "amount": sum(t.amount for t in transactions),
        }

    except TransactionServiceError as error:
        return {
            "error": "TRANSACTION_SERVICE_UNAVAILABLE",
            "message": str(error),
        }


############# Main code #################
llm = ChatOllama(
    model="llama3.2:1b"
)

tools_list = [get_account_balance,
              get_recent_transactions, calc_net_transactions]

agent = create_agent(
    model=llm,
    tools=tools_list
)

messages = [
    SystemMessage(content="You are a helpful bank AI assistant. "
                  "Be concise and never invent account information. "
                  "If a tool returns an error, clearly tell the user that "
                  "the requested information could not be retrieved. "
                  "Never invent or substitute data when a tool fails.")]

messages.append(
    HumanMessage(content="List my recent transactions")
)
# messages.append(
#     HumanMessage(content="""
#         What is my balance, and what is my net transaction amount based only on the transactions you retrieved?
#     """)
# )

current_user_context = UserContext(
    user_id=1432552
)

result = agent.invoke({"messages": messages}, context=current_user_context)

# llm_with_tools = llm.bind_tools(tools_list)

# response = llm_with_tools.invoke(messages)
# print(response.tool_calls)

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
