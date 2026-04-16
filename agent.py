import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
_client = (
    OpenAI(api_key=_DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")
    if _DEEPSEEK_API_KEY
    else None
)


def _simulate_response(text: str, temperature: float, response_style: str) -> str:
    """Local fallback when no API key is provided or an API call fails."""
    style = str(response_style).strip().lower()

    if style == "detailed":
        return (
            f"Detailed response (temperature={temperature}): You asked '{text}'. "
            "Here is a fuller simulated explanation with extra context and next steps."
        )
    if style == "humorous":
        return (
            f"Humorous response (temperature={temperature}): You asked '{text}'. "
            "My circuits chuckled, and this is your playful simulated answer."
        )

    return f"Concise response (temperature={temperature}): You asked '{text}'."


def process(user_input, temperature=0.3, response_style="Concise"):
    """Process a user request via DeepSeek (OpenAI-compatible), with fallback simulation."""
    if user_input is None:
        return "Please provide a valid input."

    text = str(user_input).strip()
    if not text:
        return "Please provide a non-empty input."

    # If the API key is missing, keep the dashboard functional using the simulation.
    if _client is None:
        return _simulate_response(text, temperature, response_style)

    try:
        system_message = (
            "You are an AI agent. "
            f"Respond using the '{response_style}' style. "
            "Keep the response directly relevant to the user's request."
        )
        completion = _client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text},
            ],
            temperature=temperature,
        )
        return completion.choices[0].message.content or ""
    except Exception:
        # Fail closed to a local simulation so the app never crashes.
        return _simulate_response(text, temperature, response_style)
