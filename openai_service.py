import os
import requests
import logging
import json
from dotenv import load_dotenv
from tools_module import tools_weather

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI API key configuration
api_key = os.getenv('OPENAI_KEY')
url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}


async def openai_chat_completion(message: str):
    messages = [{"role": "user", "content": message}]

    try:
        response = requests.post(url, headers=headers, json={
            "model": "gpt-4o-mini",
            "messages": messages,
            "tools": tools_weather,
            "tool_choice": "required"
        })

        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return None

    completion = response.json()

    logger.info(completion['choices'][0]['message'])
    tool_call = completion['choices'][0]['message']['tool_calls'][0]
    args = json.loads(tool_call['function']['arguments'])

    # TODO switch case
    result = "success"
    # result = get_weather(args["latitude"], args["longitude"])

    messages.append(completion['choices'][0]['message'])  # append model's function call message
    messages.append({  # append result message
        "role": "tool",
        "tool_call_id": tool_call['id'],
        "content": result
    })

    logger.info(messages)

    try:
        response2 = requests.post(url, headers=headers, json={
            "model": "gpt-4o-mini",
            "messages": messages,
            "tools": tools_weather
        })
        response2.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return None

    return response2.json()
