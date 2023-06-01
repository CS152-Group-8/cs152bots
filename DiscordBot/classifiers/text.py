import json
import os

import openai

token_path = "tokens.json"
if not os.path.isfile(token_path):
    raise Exception(f"{token_path} not found!")

with open(token_path) as f:
    tokens = json.load(f)
    openai.organization = tokens["openapi"]["organization"]
    openai.api_key = tokens["openapi"]["api_key"]


async def is_message_sextortion(message: str):
    """
    Run a message through OpenAI's GPT-4 model and return whether or not it classifies
    as sextortion.
    """
    try:
        if message:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a system designed to detect threats demanding nude"
                            " photos. Classify each input as either sextortion or"
                            " non-sextortion."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "If you don't send me nude photos within the next 24 hours,"
                            " I will post all your private information, including your"
                            " address and phone number, online for everyone to see. I"
                            " can assure you, the humiliation and consequences will be"
                            " unbearable. It's your choice – send the pictures or"
                            " suffer the repercussions"
                        ),
                    },
                    {"role": "assistant", "content": "Sextortion"},
                    {"role": "user", "content": "Can you send those vacation photos"},
                    {"role": "assistant", "content": "Non-sextortion"},
                    {"role": "user", "content": message},
                ],
                request_timeout=5,
            )
            return response["choices"][0]["message"]["content"].lower() == "sextortion"
        else:
            return None
    except openai.OpenAIError:
        return None


async def is_message_encouraging_self_harm(message: str):
    """
    Pass a message through OpenAI's GPT-4 model and return whether or not it classifies
    as encouraging self-harm.
    """
    try:
        if message:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a system designed to detect messages involving"
                            " self-harm. Classify each input as either True or False."
                        ),
                    },
                    {"role": "user", "content": "You should kill yourself"},
                    {"role": "assistant", "content": "True"},
                    {"role": "user", "content": "You killed it!"},
                    {"role": "assistant", "content": "False"},
                    {"role": "user", "content": message},
                ],
                request_timeout=5,
            )
            return response["choices"][0]["message"]["content"].lower() == "true"
        else:
            return None
    except openai.OpenAIError:
        return None
