import asyncio
import logging
import os

from agents import Runner
from pymongo import MongoClient

from Agents.agents_new import generate
from Agents.data import (final_update, get_chunks_for_topic,
                         get_placeholders_from_mongo, get_subject_for_unit,
                         get_topic_ids_for_unit, get_units_from_mongo,
                         update_validated_layouts)
from Agents.schema import UnitList
from Agents.utils import parse_data
from Agents.validation_agents import validator

# This is the main agentic loop which will call the generate function
mongo_client = MongoClient(os.environ.get("MONGO_URI"))

logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)


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
    logger.info(f"Got units: {units}")
    for unit in units:
        topics = get_topic_ids_for_unit(unit)
        logger.info(f"Got topics: {topics} for the unit: {unit}")
        all_layouts_for_unit = []  # New list to store layouts from all topics
        layouts_validated = []
        for topic in topics:
            content = get_chunks_for_topic(topic[0])
            layouts_processed = await generate(content[0][3], doc_id=doc_id)
            logger.info(f"Generated layouts: {layouts_processed}")
            logger.info(f"Planned layouts for the topic: {topic[0]}")
            all_layouts_for_unit.append(layouts_processed)

        try:
            all_layouts = get_placeholders_from_mongo(
                client=mongo_client, doc_id=doc_id
            )
            for layout in all_layouts:
                validated_layout = await validate_layouts(
                    layout["data"], layout["data"]["title"]
                )

                logger.info(f"Validated Layout: {validated_layout}")
                layouts_parsed = parse_data(validated_layout)
                logger.info(f"Parsed Layout: {layouts_parsed}")
                layouts_validated.append(layouts_parsed)
                update_validated_layouts(
                    mongo_client,
                    doc_id,
                    layouts_validated,
                    "validating layouts",
                )

        except Exception as e:
            print(f"Error in validating content: {e}")
            update_validated_layouts(
                mongo_client,
                doc_id,
                [],  # Pass an empty list or handle differently
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
