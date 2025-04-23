import asyncio
import os

from agents import Runner
from pymongo import MongoClient

from Agents.agents_new import generate
from Agents.data import (final_update, get_chunks_for_topic,
                         get_subject_for_unit, get_topic_ids_for_unit,
                         insert_doc, update_validated_layouts)
from Agents.schema import UnitList
from Agents.utils import parse_content_output
from Agents.validation_agents import validator

# This is the main agentic loop which will call the generate function

mongo_client = MongoClient(os.environ.get("MONGO_URI"))


async def validate_layouts(layout, content):
    """Async function to validate a layout."""
    validated_layout = await Runner.run(
        validator,
        f"Validate the slide layout {layout} with the schema of layouts given on the content {content}",
    )
    return validated_layout.final_output


def main(units: UnitList):
    """
    Main function to run the agentic loop.
    :param units: List of units to process.
    """
    subject = get_subject_for_unit(units.units[0])
    doc_id = insert_doc(
        mongo_client,
        userId=units.userId,
        subject=subject,
    )
    print(f"Document ID: {doc_id}")

    for unit in units.units:
        topics = get_topic_ids_for_unit(unit)
        layouts_validated = []
        all_layouts_for_unit = []  # New list to store layouts from all topics
        for topic in topics:
            print(topic[0])
            content = get_chunks_for_topic(topic[0])
            layouts_processed = asyncio.run(generate(content[0][3], doc_id=doc_id))
            all_layouts_for_unit.append(layouts_processed)

        # Validate the layouts for the entire unit
        try:
            for layout in all_layouts_for_unit:
                validated_layout = asyncio.run(validate_layouts(layout, content[0][3]))
                print(validated_layout.final_output)
                parsed_validated_layout = parse_content_output(
                    validated_layout.final_output
                )
                print(parsed_validated_layout)
                print("\n\n")
                layouts_validated.append(
                    parsed_validated_layout
                )  # Append the validated layout
                update_validated_layouts(
                    mongo_client,
                    doc_id,
                    parsed_validated_layout,  # Pass the single validated layout
                    "validating layouts",
                )

        except Exception as e:
            print(f"Error in validating content: {e}")
            # Update with an empty list or handle error state appropriately
            update_validated_layouts(
                mongo_client,
                doc_id,
                [],  # Pass an empty list or handle differently
                "failed during content validation",
                str(e),
            )
            return  # Or continue depending on desired error handling

        # Use the complete list of validated layouts for the final update
        final_update(
            mongo_client,
            placeholders=layouts_validated,
            doc_id=doc_id,
            status="completed",
        )


if __name__ == "__main__":
    main(
        UnitList(
            units=[10],
            userId="user_123",
        )
    )
