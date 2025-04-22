import os

from agents import Agent, ModelSettings, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.environ.get("GEMINI_API_KEY"),
)

validator = Agent(
    name="Validator",
    instructions="",
    model=OpenAIChatCompletionsModel("gemini-2.0-flash-001", openai_client=client),
    model_settings=ModelSettings(temperature=0.6, tool_choice="required"),
)
