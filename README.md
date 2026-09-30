# Customer Support Chatbot

A local AI-powered customer support chatbot built with Python, FastAPI, Ollama, SQLite, HTML, CSS, and JavaScript.

## Features

* AI-powered customer support
* Local LLM using Ollama
* FastAPI backend
* SQLite conversation storage
* Conversation history
* Web-based chat interface
* REST API
* No paid AI API required

## Technology Stack

* Python
* FastAPI
* Uvicorn
* Ollama
* SQLite
* HTML
* CSS
* JavaScript

## Project Structure

```text
customer-chatbot/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   └── chatbot.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── data/
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

* Windows 10/11
* Python 3.11+
* Ollama

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/customer-chatbot.git
cd customer-chatbot
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Install Ollama Model

Install Ollama and download the model:

```powershell
ollama pull llama3.2
```

Start Ollama:

```powershell
ollama serve
```

## Run the Application

Open another PowerShell window and activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start FastAPI:

```powershell
python -m uvicorn backend.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Database

The application automatically creates:

```text
data/chatbot.db
```

The database stores conversations and chat messages.

## Future Improvements

* Customer authentication
* Order tracking
* Product database
* FAQ knowledge base
* Admin dashboard
* Human-agent escalation
* Authentication and authorization
* Prompt-injection detection
* PII protection
* LLM output validation
* Docker deployment
* Cloud deployment

## License

For educational and portfolio use.
