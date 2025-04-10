import asyncio
import os

from openai import AsyncOpenAI
from prompts import Content, Layouts, Planner_Prompt
from pydantic.type_adapter import P
from schema import PlannerOutput

from agents import (Agent, ModelSettings, OpenAIChatCompletionsModel, Runner,
                    handoff, set_default_openai_api, set_default_openai_client)

set_default_openai_api("chat_completions")


client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.environ.get("GEMINI_API_KEY"),
)


create_slide = Agent(
    name="Create Slide",
    instructions="You are an expert slide designer. Create a slide based on the layout provided.",
    model=OpenAIChatCompletionsModel("gemini-2.0-flash", openai_client=client),
    model_settings=ModelSettings(temperature=0.8),
)

planner = Agent(
    name="Slide Layout Planner",
    instructions=Planner_Prompt.format(
        templates=Layouts,
        content=Content,
    ),
    model=OpenAIChatCompletionsModel("gemini-2.0-flash-001", openai_client=client),
    model_settings=ModelSettings(temperature=0.6),
    output_type=list[PlannerOutput],
)


async def main():
    layout_result = await Runner.run(
        planner,
        "Create a slide layout for a presentation on the impact of climate change on biodiversity.",
    )
    layout = layout_result.final_output
    print("Planner's Slide Layout:\n", layout)


if __name__ == "__main__":
    asyncio.run(main())
