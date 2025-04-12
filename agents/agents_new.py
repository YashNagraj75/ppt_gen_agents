import asyncio
import os

from openai import AsyncOpenAI
from prompts import Content, Layout_Desc, Planner_Prompt
from schema import PlannerOutput
from utils import encode_images

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
        templates=Layout_Desc,
        content=Content,
    ),
    model=OpenAIChatCompletionsModel("gemini-2.0-flash-001", openai_client=client),
    model_settings=ModelSettings(temperature=0.9),
    output_type=list[PlannerOutput],
)


async def main():
    images_data = encode_images()
    content = [
        {
            "type": "input_text",
            "text": "Create a slide layout for a presentation on the impact of climate change on biodiversity. And these are the images of the slide layouts for you to get a better visual understanding of the slide layouts.",
        },
    ]
    for relative_path, image_data in images_data.items():
        content.append(
            {
                "type": "input_image",
                "image_url": image_data["url"],
                "detail": image_data["detail"],
            },
        )
    layout_result = await Runner.run(
        planner,
        input=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )
    layouts = layout_result.final_output

    # Print just the layout information without the base64 encoded images
    for layout in layouts:
        print(f"Layout: {layout.layout}, Title: {layout.title}")


if __name__ == "__main__":
    asyncio.run(main())
