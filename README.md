# ProductivityAgent 📬🤖

An AI-powered personal assistant that integrates with your email and messaging tools to analyze communication, suggest smart actions, and gradually act more like you.

---

## 🧭 Table of Contents

- [ProductivityAgent 📬🤖](#productivityagent-)
  - [🧭 Table of Contents](#-table-of-contents)
  - [🧠 Introduction](#-introduction)
  - [🛠️ Current Capabilities](#️-current-capabilities)
  - [📂 Project Structure](#-project-structure)
  - [▶️ How to Run](#️-how-to-run)
  - [📅 Development Diary](#-development-diary)
  - [💡 Future Ideas](#-future-ideas)
  - [📬 Contact](#-contact)

---

## 🧠 Introduction

**ProductivityAgent** is an AI personal assistant project built with LangChain, LangSmith, and email APIs (Gmail, Outlook in progress).  
Its main goal is to automate and assist with knowledge work by analyzing email threads, extracting meaning, and taking actions like:

1. ✅ Suggesting answers in your tone and style.
2. ✅ Detecting implicit tasks and syncing them with your task manager (planned).
3. ✅ Preparing smart agendas before meetings (planned).
4. ✅ Detecting conflicts, opportunities, and key issues among participants (planned).
5. ✅ Acting like you progressively using LangGraph and memory.

This is a long-term assistant designed to evolve.

---

## 🛠️ Current Capabilities

| Feature                        | Status       | Notes |
|-------------------------------|--------------|-------|
| Gmail integration             | ✅ Done       | Reads recent emails and searches by keyword |
| LangChain Tools               | ✅ Done       | Agent can call tools like `get_gmail_summary` or `search_gmail_by_keyword` |
| Email parsing (metadata)      | ✅ Done       | Extracts structured data from raw emails |
| LangSmith tracking            | ✅ Done       | Agent is tracked for debugging and improvement |
| Outlook integration           | 🚧 Blocked    | Waiting for IT admin approval |
| Task extraction (from emails) | ⏳ Upcoming   | NLP analysis for task detection |
| Agenda generator              | ⏳ Upcoming   | Based on calendar/emails before meetings |

---

## 📂 Project Structure

```bash
ProductivityAgent/
│
├── agent/
│   ├── agent_runner.py       # Main LangChain agent logic
│   ├── tools.py              # LangChain tools used by the agent
│   ├── config.py             # API Keys and Env config
│
├── utils/
│   ├── gmail_client.py       # Gmail API logic
│   ├── outlook_client.py     # Outlook integration (in progress)
│   ├── email_parser.py       # Utility to parse raw email strings
│
├── test_gmail.py             # Run standalone Gmail test
├── test_outlook.py           # Run standalone Outlook test
├── main.py                   # Entry point for the agent
├── .env                      # Credentials (excluded from git)
├── credentials.json          # Gmail OAuth2 config
├── requirements.txt
```

---

## ▶️ How to Run

1. Create a `.env` file with the necessary variables (see example below).
2. Copy .env.example to .env and fill in your credentials to get started.
3. Set up your Gmail credentials in `credentials.json` (download from Google Cloud Console).
4. Run `test_gmail.py` to validate your Gmail setup.
5. Run `main.py` to launch the agent.

```env
# Gmail uses local token.pickle after first login
LANGSMITH_API_KEY=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=...
AZURE_OPENAI_DEPLOYMENT_NAME=...
AZURE_OPENAI_API_VERSION=...
```

---

## 📅 Development Diary

| Date        | Update                                                                 |
|-------------|------------------------------------------------------------------------|
| 2025-03-27 | 🧠 Project recap, cleaned tools, LangSmith enabled, and Gmail integrated |
| 2025-03-27  | ✅ Gmail client working with OAuth and token.pickle persistency         |
| 2025-03-26  | 🧪 Gmail API authorization flow setup completed                         |
| 2025-03-25  | 🛠️ Initial LangChain agent created using ReAct + Tavily search          |

---

## 💡 Future Ideas

- Integrate with Google Calendar and MS Teams.
- Train a fine-tuned LLM based on your writing tone.
- Add feedback learning loop using LangSmith traces.
- Automatic tagging and smart archiving of emails.
- Conversational agent interface (voice/chat/web).
- Priority detection + meeting preparation features.

---

## 📬 Contact

Built by Pol Fernández (pol.fernandez.blanquez@gmail.com)  
Follow my journey on [GitHub](https://github.com/polfernandezblanquez) or LinkedIn soon.
