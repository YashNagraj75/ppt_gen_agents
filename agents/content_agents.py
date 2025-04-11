from agents_new import client

from agents import Agent, ModelSettings, OpenAIChatCompletionsModel, handoff

chart_agent = Agent(
    name="Chart Generator",
    instructions="",
    model=OpenAIChatCompletionsModel("gemini-2.0-flash-001", openai_client=client),
    model_settings=ModelSettings(temperature=0.6),
)

text_agent = chart_agent.clone(
    name="Content Generator",
    instructions="Make content",
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
    instructions="",
    model=OpenAIChatCompletionsModel("gemini-2.0-flash-001", openai_client=client),
    model_settings=ModelSettings(temperature=0.6),
    handoffs=[
        handoff(chart_agent),
        handoff(text_agent),
        handoff(table_agent),
        handoff(image_agent),
        handoff(media_agent),
    ],
)
