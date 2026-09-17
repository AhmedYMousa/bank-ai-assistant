## 1. Create the virtual environment:
.venv => is the virtual Env name
```
python -m venv .venv
```

## 2. Activate it
If you're using Git Bash on Windows
```
source .venv/Scripts/activate
```



## 3. Give the assistant instructions
we can provide different message roles:
- System → instructions for the assistant
- Human → the user's message
- AI → previous assistant responses




## 4. Multi-turn conversation
The model itself doesn't automatically remember previous calls to `invoke()`. We need to provide the previous messages as part of the next request.
So when we say an LLM has "conversation memory", at this basic level we're really talking about providing previous messages as context.



## 5. Execute the tool and return the result to the LLM
from langchain.agents import create_agent
```
agent = create_agent(
    model=llm,
    tools=[get_account_balance],
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Get my current account balance."
            }
        ]
    }
)

print(result["messages"][-1].content)
```


## Work with Pydantic
Pydantic is a Python library for data validation and structured data parsing.

The easiest way to think about it:

Pydantic lets you define what your data should look like, and then validates incoming data against that definition.