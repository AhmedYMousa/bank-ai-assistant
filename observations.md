## The same input can produce different outputs.

You didn't change:

the tools
the tool descriptions
the user prompt
the model
the code

Yet you got different results.

### This gives us our first real Agent lesson

We should now introduce an important distinction:

Tool correctness

The tool should be deterministic and authoritative:

```
Tool → actual bank data
```

Model correctness

The model should accurately interpret and communicate that data:

```
Tool result → LLM → response
```

Those are different things and need different tests.

## An LLM is not a calculator, even when the arithmetic is trivial.

That's not a tool failure. The tool gave the correct data.

It's the LLM trying to perform arithmetic during generation.

### 📝 This leads to a very important Agent design principle

`Don't ask the LLM to perform operations that your application can perform deterministically.`

                    ┌──────────────┐
                    │     LLM      │
                    │ Reasoning /  │
                    │ language     │
                    └──────┬───────┘
                           │
                  delegates deterministic
                       operations
                           │
                           ▼
                    ┌──────────────┐
                    │    Tools     │
                    │              │
                    │ DB queries   │
                    │ calculations │
                    │ APIs         │
                    └──────────────┘

But in a real banking system, I'd be very careful about asking the LLM to calculate:

balances
totals
interest
fees
transaction amounts
available credit
exchange rates

Those should generally come from authoritative application logic, not LLM arithmetic.

## Tool contracts vs. LLM contracts

Changing the contract from Pydantic model to an LLM friendly description json made the LLM provide correct answers. The last AIMessage when I was using Pydantic model was giving me "I can't find your transactions" even though the ToolMessage response is showing them.
