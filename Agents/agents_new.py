import os

from agents import (
    Agent,
    ModelSettings,
    OpenAIChatCompletionsModel,
    Runner,
    set_default_openai_api,
)
from google.cloud import logging
from openai import AsyncOpenAI
from pymongo import MongoClient

from .content_agents import content_formatter, content_generator
from .data import update_layouts, update_placeholders
from .prompts import Content_Generator, Layout_Desc, Planner_Prompt
from .schema import PlannerOutput
from .tools import encode_images
from .utils import parse_data, parse_planner_output

set_default_openai_api("chat_completions")
log_client = logging.Client(project="edunova-455712")
logger = log_client.logger("generator_logs")


mongo_client = MongoClient(os.environ.get("MONGO_URI"))

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
    model=OpenAIChatCompletionsModel(
        "gemini-2.5-flash-preview-05-20", openai_client=client
    ),
    instructions=Planner_Prompt.format(
        templates=Layout_Desc,
    ),
    model_settings=ModelSettings(temperature=0.9, reasoning=True),
    output_type=list[PlannerOutput],
)


async def generate(syllabus_content: str = None, doc_id: str = None):
    layouts_planned = []
    layouts_processed = []
    try:
        images_data = encode_images()
        content = [
            {
                "type": "input_text",
                "text": f"Make slides on the content {syllabus_content}",
            },
        ]
        for _, image_data in images_data.items():
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
        parsed_layouts = parse_planner_output(layouts)
        layouts_planned.append(parsed_layouts)
        logger.log_text(f"Layouts planned: {layouts_planned}")
        print(f"Layouts planned: {layouts_planned}")
        update_layouts(
            mongo_client,
            doc_id,
            layouts_planned,
            "layouts_planned",
        )
    except Exception as e:
        print(f"Error in generating layout: {e}")
        update_layouts(
            mongo_client,
            doc_id,
            [],
            "failed during layout planning",
            str(e),
        )
        return

    try:
        for layout in layouts:
            content_generator.instructions = Content_Generator.format(
                layout_name=layout.layout,
                title=layout.title,
                content=syllabus_content,
                layouts=Layout_Desc,
            )
            content = await Runner.run(content_generator, "Make the slide layout")
            logger.log_text(f"Content generated: {content}")
            print(f"Content generated: {content}")
            formatted_content = await Runner.run(
                content_formatter,
                f"Format this {content.final_output} to output schema",
            )
            logger.log_text(f"Formatted output: {formatted_content.final_output}")
            print(f"Formatted output: {formatted_content.final_output}")
            parsed_content = parse_data(formatted_content.final_output)
            layouts_processed.append(parsed_content)
            logger.log_text(f"Layouts processed: {layouts_processed}")
            print(f"Layouts processed: {layouts_processed}")
            update_placeholders(
                mongo_client,
                doc_id,
                layouts_processed,
                "processing_layouts",
            )
    except Exception as e:
        print(f"Error in generating content: {e}")
        update_placeholders(
            mongo_client,
            doc_id,
            [],
            "failed during content generation",
            str(e),
        )
        return

    return layouts_processed
