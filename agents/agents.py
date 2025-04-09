import os

from openai import AsyncOpenAI

from agents import set_default_openai_client

client = AsyncOpenAI(
    api_key=os.environ.get("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_default_openai_client(client)
