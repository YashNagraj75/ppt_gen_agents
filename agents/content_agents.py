import os

from openai import AsyncOpenAI
from prompts import Text_Prompt

from agents import Agent, ModelSettings, OpenAIChatCompletionsModel, handoff

# Create the client here instead of importing from agents_new
client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.environ.get("GEMINI_API_KEY"),
)

chart_agent = Agent(
    name="Chart Generator",
    instructions="",
    model=OpenAIChatCompletionsModel("gemini-2.0-flash-001", openai_client=client),
    model_settings=ModelSettings(temperature=0.6),
)

text_agent = chart_agent.clone(
    name="Text Generator",
    instructions=Text_Prompt,
)

table_agent = chart_agent.clone(
    name="Table Generator",
    instructions="Generate tables",
)

image_agent = chart_agent.clone(
    name="Table Generator",
    instructions="Generate tables",
)

media_agent = chart_agent.clone(
    name="Table Generator",
    instructions="Generate tables",
)

content_generator = Agent(
    name="Content Generator",
    model=OpenAIChatCompletionsModel("gemini-2.0-flash-001", openai_client=client),
    model_settings=ModelSettings(temperature=0.6, tool_choice="required"),
    tools=[
        text_agent.as_tool(
            tool_name="text_placeholder_content_generation",
            tool_description="Use this tool for getting text for the content in the slide layout",
        )
    ],
)
