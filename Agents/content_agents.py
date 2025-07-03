import os

import google.auth.transport.requests
from agents import (Agent, ModelSettings, OpenAIChatCompletionsModel,
                    model_settings)
from google.auth import default
from openai import AsyncOpenAI

from .prompts import (Chart_Prompt, Formatter_Prompt, Image_Prompt,
                      Input_String, Layout_Desc, Media_Prompt, Output_String,
                      Table_Prompt, Text_Prompt)
from .schema import ContentOutput
from .tools import get_image_description, get_video_and_transcript

# Create the client here instead of importing from agents_new
credentials, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(google.auth.transport.requests.Request())

client = AsyncOpenAI(
    base_url="https://us-central1-aiplatform.googleapis.com/v1/projects/edunova-455712/locations/us-central1/endpoints/openapi",
    api_key=credentials.token,
)

chart_agent = Agent(
    name="Chart Generator",
    instructions=Chart_Prompt,
    model=OpenAIChatCompletionsModel("google/gemini-2.0-flash", openai_client=client),
    model_settings=ModelSettings(temperature=0.6),
)

text_agent = chart_agent.clone(
    name="Text Generator",
    instructions=Text_Prompt,
)

table_agent = chart_agent.clone(
    name="Table Generator",
    instructions=Table_Prompt,
)

image_agent = chart_agent.clone(
    name="Image Generator",
    instructions=Image_Prompt,
    tools=[
        get_image_description,
    ],
)


media_agent = chart_agent.clone(
    name="Media Generator",
    instructions=Media_Prompt,
    tools=[
        get_video_and_transcript,
    ],
)

content_generator = Agent(
    name="Content Generator",
    model=OpenAIChatCompletionsModel(
        "google/gemini-2.5-flash-preview-05-20", openai_client=client
    ),
    model_settings=ModelSettings(temperature=0.8, tool_choice="required"),
    tools=[
        text_agent.as_tool(
            tool_name="text_placeholder_content_generation",
            tool_description="Use this tool for getting text for the content in the slide layout",
        ),
        image_agent.as_tool(
            tool_name="image_placeholder_content_generation",
            tool_description="Use this tool for getting image for the content in the slide layout",
        ),
        table_agent.as_tool(
            tool_name="table_placeholder_content_generation",
            tool_description="Use this tool for getting table for the content in the slide layout",
        ),
        chart_agent.as_tool(
            tool_name="chart_placeholder_content_generation",
            tool_description="Use this tool for getting chart for the content in the slide layout",
        ),
        media_agent.as_tool(
            tool_name="media_placeholder_content_generation",
            tool_description="Use this tool for getting video links for the content in the slide layout",
        ),
    ],
)

content_formatter = Agent(
    name="Content Formatter",  # Changed name from "Chart Generator" to more accurate "Content Formatter"
    instructions=Formatter_Prompt,
    model=OpenAIChatCompletionsModel("google/gemini-2.0-flash", openai_client=client),
    model_settings=ModelSettings(temperature=0.6),
    output_type=ContentOutput,
)
