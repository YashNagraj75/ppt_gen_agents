import os

from agents import Agent, ModelSettings, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

from .prompts import Layout_Desc, Validator_Prompt
from .schema import ContentOutput

client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.environ.get("GEMINI_API_KEY"),
)

validator = Agent(
    name="Validator",
    instructions=Validator_Prompt.format(layouts=Layout_Desc),
    model=OpenAIChatCompletionsModel(
        "gemini-2.5-flash-preview-05-20", openai_client=client
    ),
    model_settings=ModelSettings(temperature=0.8),
    output_type=ContentOutput,
)
