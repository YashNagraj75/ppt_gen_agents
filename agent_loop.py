import asyncio
import os

import bson
from pymongo import MongoClient

from Agents.agents_new import generate
from Agents.data import (get_chunks_for_topic, get_subject_for_unit,
                         get_topic_ids_for_unit, get_topics_for_unit,
                         insert_doc)
from Agents.schema import UnitList

# This is the main agentic loop which will call the generate function

mongo_client = MongoClient(os.environ.get("MONGO_URI"))


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
        for topic in topics:
            print(topic[0])
            content = get_chunks_for_topic(topic[0])
            asyncio.run(generate(content[0][3], doc_id=doc_id))


if __name__ == "__main__":
    main(
        UnitList(
            units=[6],
            userId="user_123",
        )
    )
