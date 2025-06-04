import os

from agents import Agent, ModelSettings, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from google.auth import default
import google.auth.transport.requests

from .prompts import Layout_Desc, Validator_Prompt
from .schema import ContentOutput

credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())

client = AsyncOpenAI(
    base_url="https://us-central1-aiplatform.googleapis.com/v1/projects/edunova-455712/locations/us-central1/endpoints/openapi",
    api_key=credentials.token,
)

validator = Agent(
    name="Validator",
    instructions=Validator_Prompt.format(layouts=Layout_Desc),
    model=OpenAIChatCompletionsModel("google/gemini-2.0-flash", openai_client=client),
    model_settings=ModelSettings(temperature=0.8),
    output_type=ContentOutput,
)
