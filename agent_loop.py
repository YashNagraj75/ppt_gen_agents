import asyncio
import os
import sys

from agents import Runner
from google.cloud import logging
from pymongo import MongoClient

from Agents.agents_new import generate
from Agents.data import (final_update, get_chunks_for_topic,
                         get_placeholders_from_mongo, get_topic_ids_for_unit,
                         get_units_from_mongo, update_validated_layouts)
from Agents.utils import parse_data
from Agents.validation_agents import validator

# This is the main agentic loop which will call the generate function
mongo_client = MongoClient(os.environ.get("MONGO_URI"))

log_client = logging.Client(project="edunova-455712")
logger = log_client.logger("batch_task_logs")


async def validate_layouts(layout, content):
    """Async function to validate a layout."""
    validated_layout = await Runner.run(
        validator,
        f"Validate the slide layout {layout} with the schema of layouts given on the content {content}",
    )
    return validated_layout.final_output


async def main(doc_id: str):
    units = get_units_from_mongo(
        client=mongo_client,
        doc_id=doc_id,
    )
    logger.log_text(f"Got units: {units}")
    print(f"Got units: {units}")
    for unit in units:
        topics = get_topic_ids_for_unit(unit)
        print(f"Got topics: {topics} for the unit: {unit}")
        logger.log_text(f"Got topics: {topics} for the unit: {unit}")
        all_layouts_for_unit = []  # New list to store layouts from all topics
        layouts_validated = []
        for topic in topics:
            content = get_chunks_for_topic(topic[0])
            print(f"Got content for the topic: {topic[0]}")
            layouts_processed = await generate(content[0][3], doc_id=doc_id)
            logger.log_text(f"Generated layouts: {layouts_processed}")
            logger.log_text(f"Planned layouts for the topic: {topic[0]}")
            all_layouts_for_unit.append(layouts_processed)

        try:
            all_layouts = get_placeholders_from_mongo(
                client=mongo_client, doc_id=doc_id
            )
            for layout in all_layouts:
                validated_layout = await validate_layouts(
                    layout["data"], layout["data"]["title"]
                )

                logger.log_text(f"Validated Layout: {validated_layout}")
                try:
                    layouts_parsed = parse_data(validated_layout)
                    layouts_validated.append(layouts_parsed)
                    logger.log_text(f"Parsed Layout: {layouts_parsed}")
                except Exception as parse_error:
                    print(f"Error parsing validation result: {parse_error}")
                    logger.log_text(f"Error parsing validation result: {parse_error}")
                    print(f"Raw validation result: {validated_layout}")
                    logger.log_text(f"Raw validation result: {validated_layout}")
                    continue
                layouts_validated.append(layouts_parsed)
                update_validated_layouts(
                    mongo_client,
                    doc_id,
                    layouts_validated,
                    "validating_layouts",
                )

        except Exception as e:
            print(f"Error in validating content: {e}")
            update_validated_layouts(
                mongo_client,
                doc_id,
                [],
                "failed during content validation",
                str(e),
            )
            return

        # Use the complete list of validated layouts for the final update
        final_update(
            mongo_client,
            doc_id=doc_id,
            status="completed",
        )
        return "success"


async def run_and_cleanup(doc_id: str):
    result = await main(doc_id)
    if result != "success":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: agent_loop.py <doc_id>", file=sys.stderr)
        sys.exit(1)
    _, doc_id = sys.argv
    print(f"Running agent loop for doc_id: {doc_id}")
    asyncio.run(run_and_cleanup(doc_id))
