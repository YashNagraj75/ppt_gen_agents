import asyncio
import os

from openai import AsyncOpenAI

from agents import (Agent, ModelSettings, OpenAIChatCompletionsModel, Runner,
                    set_default_openai_api, set_default_openai_client)

set_default_openai_api("chat_completions")

client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.environ.get("GEMINI_API_KEY"),
)


ModelSettings.tool_choice = "auto"

planner = Agent(
    name="Slide Layout Planner",
    instructions="You are an expert slide layout designer give slide layouts given the content for the presentation",
    model=OpenAIChatCompletionsModel(
        "gemini-2.0-flash-thinking-exp-01-21", openai_client=client
    ),
)


async def main():
    result = await Runner.run(
        planner,
        "Create a slide layout for a presentation on the impact of climate change on biodiversity.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
