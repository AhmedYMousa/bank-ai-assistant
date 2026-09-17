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
