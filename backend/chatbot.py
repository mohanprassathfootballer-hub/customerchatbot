import httpx


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "llama3.2"


SYSTEM_PROMPT = """
You are a professional customer support chatbot.

Your responsibilities:
- Answer customer questions clearly and politely.
- Be concise but helpful.
- Help customers with products, orders, returns, refunds, shipping,
  payments, and general support.
- If you do not know something, say that you do not have enough information.
- Never invent order numbers, prices, delivery dates, refund status,
  customer information, or company policies.
- Do not request passwords, API keys, credit card numbers, or other secrets.
- If a customer needs a human agent, politely recommend contacting support.
"""


async def generate_response(messages):

    ollama_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    for message in messages:
        ollama_messages.append(
            {
                "role": message["role"],
                "content": message["message"]
            }
        )

    payload = {
        "model": MODEL,
        "messages": ollama_messages,
        "stream": False
    }

    async with httpx.AsyncClient(timeout=120.0) as client:

        response = await client.post(
            OLLAMA_URL,
            json=payload
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]["content"]