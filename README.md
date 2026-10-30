# The Smallest Agent

The shortest possible AI agent with the **Claude Agent SDK**: **7 lines of Python**, plus 2 optional lines that hide a warning. It sends `Hello world!` to Claude and prints the answer.

```
Hello! 👋 How can I help you today?
```

Start here. Every other app in this repo is these 7 lines plus something more.

## Prompt for createing this application with VSCode + Claude Code Extension from Zero

```
Build a minimal Python app called "The Smallest Agent" in this (empty) folder using the Claude Agent SDK (package: claude-agent-sdk). It's a teaching example for beginners: the first app in a series where each later app adds one feature on top of this one.

## What the app does
- Sends the prompt "Hello world!" to Claude through the Agent SDK and prints only the final answer to the console.
- Ignores all the intermediate messages the SDK streams back, and prints just the final result.
- Uses the SDK defaults (no options): default model and default tools.

## Code requirements
- One file, agent.py, as short as possible: aim for about 7 lines of real logic. Import only what's needed from the SDK.
- Use the SDK's simple one-shot API (not the interactive client class), with asyncio.
- The API key comes from the ANTHROPIC_API_KEY environment variable. Never hard-code it.
- When the user is also logged in to Claude Code with a claude.ai account, the agent shows a warning at startup: "claude.ai connectors are disabled because ANTHROPIC_API_KEY or another auth source is set". Hide it by turning claude.ai MCP connectors off from inside the script before the agent starts. Keep this as clearly optional (about 2 lines with a short comment), separate from the core logic.
- requirements.txt lists only the SDK.
- Add a .gitignore for .venv, __pycache__, and .env.

## README.md (for absolute beginners)
- Short intro and the expected output.
- Part 1, configure and run: prerequisites (Python 3.10+, an API key from https://platform.claude.com/), how to get a key and add credits, a warning to treat the key like a password, creating a venv and installing on Windows PowerShell, setting the key (PowerShell and macOS/Linux), running the app.
- Part 2, how it was built: show the final agent.py and explain it step by step, one snippet per step, in plain language (async, environment variables, what the SDK imports are, the message stream, why only the last message is printed, the optional warning lines). End with a small ASCII diagram of the flow.
- A cost note: measure what one run costs with the default tools versus with built-in tools turned off, and explain why the difference exists.
- An "Exercises" section with 4–5 small extensions (change the prompt, print every message type, read the prompt from the command line, reduce cost by turning off the tools, choose a model). Each one gets a hint and a collapsible solution.
- Make sure every internal link in the README points to a heading that exists.

## Process
1. Before writing code, check the current claude-agent-sdk documentation for the right function and class names and the options, and use what it says, not what you remember.
2. Show me the plan first.
3. After writing the files, create a .venv, install the dependencies, and run the app to check that it prints a greeting. If ANTHROPIC_API_KEY isn't set, tell me how to set it. Don't ask me to paste the key into the chat.
4. Use the real cost numbers from your runs in the README cost note.
5. Initialize git and make a first commit, with no .venv and no secrets.
```

---

## Part 1: Configure and run the app

### Step 1: Check the prerequisites

| You need | How to check | Get it |
|---|---|---|
| Python 3.10 or newer | `python --version` | <https://www.python.org/downloads/> |
| A Claude API key | — | Step 2 below |

### Step 2: Get an API key

1. Sign in at <https://platform.claude.com/>.
2. Add some credits in **Settings → Billing**. One run of this app costs about **5 cents** (see [Exercise 4](#exercises) to make it much cheaper).
3. Create a key in **API Keys** and copy it. It starts with `sk-ant-`.

> ⚠️ **Treat the key like a password.** Never paste it into your code, and never commit it to Git.

### Step 3: Create a virtual environment and install the SDK

Open a terminal **in this folder** (`00-python-minimal`).

**Windows (PowerShell)**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> 💡 If you already created the shared `.venv` in the main `sample1` folder, you can use it instead: `..\.venv\Scripts\Activate.ps1`

### Step 4: Set your API key

```powershell
# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

```bash
# macOS / Linux
export ANTHROPIC_API_KEY=sk-ant-...
```

### Step 5: Run it

```powershell
python agent.py
```

After a few seconds, Claude's answer appears:

```
Hello! 👋 How can I help you today?
```

---

## Part 2: How the application was built

This is the whole program, [agent.py](agent.py):

```python
import asyncio
import os
from claude_agent_sdk import query, ResultMessage

os.environ["ENABLE_CLAUDEAI_MCP_SERVERS"] = "false"  # Hide the "claude.ai connectors are disabled" warning

async def main():
    async for message in query(prompt="Hello world!"):
        if isinstance(message, ResultMessage):
            print(message.result)

asyncio.run(main())
```

The agent itself is **7 lines**. The 2 lines with `os` only hide a warning. Let's go through it step by step.

### Step 1: import `asyncio` and `os`

```python
import asyncio
import os
```

Both are part of Python:

- `asyncio` runs **asynchronous** code: code that waits for something, here Claude's answer, without freezing the program.
- `os` lets the program read and change **environment variables** (see Step 3).

### Step 2: import from the SDK

```python
from claude_agent_sdk import query, ResultMessage
```

We need only two things from the SDK:

| Name | What it is |
|---|---|
| `query` | Starts the agent and sends it your prompt |
| `ResultMessage` | The last message the agent sends, with the final answer |

### Step 3: hide the connectors warning (optional)

```python
os.environ["ENABLE_CLAUDEAI_MCP_SERVERS"] = "false"  # Hide the "claude.ai connectors are disabled" warning
```

If you're also logged in to **Claude Code** with your claude.ai account, the agent shows this warning when it starts:

```
⚠ claude.ai connectors are disabled because ANTHROPIC_API_KEY or another auth source is set ...
```

It's harmless: the agent uses your **API key**, so it skips your claude.ai connectors and tells you so. Setting the environment variable `ENABLE_CLAUDEAI_MCP_SERVERS` to `"false"` turns those connectors off on purpose, so there's nothing to warn about. The agent reads the variable when it starts, so it must be set **before** `query()` runs.

If you're not logged in to Claude Code, you never see the warning, and you can delete this line and `import os`.

### Step 4: create an async function

```python
async def main():
```

`async def` creates a function that can **wait** (for Claude) inside it.

### Step 5: send the prompt

```python
    async for message in query(prompt="Hello world!"):
```

- `query(prompt="Hello world!")` starts the agent with your prompt.
- The agent answers with a **stream of messages** while it works, and `async for` reads them one at a time.

We pass **no options**, so the SDK uses its defaults: its default model, and its default set of built-in tools. To answer *"Hello world!"*, Claude doesn't need any tool. If it tried one that changes something (like editing a file), the call would be **denied**, because nobody is there to approve it.

> 💰 **Short code isn't always cheap code.** With the defaults, every request also sends Claude the descriptions of all the built-in tools. In testing this run cost about **$0.05**, while the same prompt with `tools=[]` cost about **$0.003**, more than **10 times less**. See [Exercise 4](#exercises).

### Step 6: print only the final answer

```python
        if isinstance(message, ResultMessage):
            print(message.result)
```

Many messages arrive (setup, Claude's thoughts, its text…). The **last** one is always a `ResultMessage`, and its `.result` field is the final answer. `isinstance()` checks the message type, so we print only that one.

### Step 7: start the program

```python
asyncio.run(main())
```

`main()` is an `async` function, so `asyncio.run()` starts it and waits until it finishes.

### Recap

```
asyncio.run(main())
   └── main()
         └── query("Hello world!") ── sends ──► Claude
               │                                 │
               ◄────── stream of messages ───────┘
               └── ResultMessage? ──► print(message.result)
```

That's a complete agent: **a prompt in, a stream of messages out**.


