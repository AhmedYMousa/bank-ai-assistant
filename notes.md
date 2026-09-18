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

## Make the LLM's job smaller

1. Understand the user's question
2. Select tools
3. Interpret tool results
4. Associate each result with its meaning
5. Produce the final answer

# dataclasses

is a built-in Python module for creating classes that mainly exist to store data.

You can think of it as a convenient way to create objects like DTOs / models without writing a lot of boilerplate code.

Without dataclass

```
class User:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

user = User("Ahmed", 36, "ahmed@example.com")
```

You have to manually write the **init**.

With dataclass

```
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str

user = User("Ahmed", 36, "ahmed@example.com")
```

## Injecting UserContext in Tool calling

Why this is different from putting the ID in the prompt

Don't do:

```
System:
The current user is user-123.
```

and expect the model to faithfully use it.

The model could potentially:

- ignore it
- hallucinate another ID
- expose it
- pass a user-supplied ID instead

<h3>📝 Runtime context creates a trusted application → tool boundary.</h3>
