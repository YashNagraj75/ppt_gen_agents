import sqlite3
from datetime import datetime

import pytz
from bson import ObjectId


# SQLite functions
def get_topics_for_unit(unit_id: int):
    try:
        conn = sqlite3.connect("knowledge-base.db")
        cursor = conn.cursor()

        cursor.execute(f"SELECT * from topics where unit_id={unit_id}")
        rows = cursor.fetchall()
        print(rows)
        return rows

    except sqlite3.Error as e:
        print(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_chunks_for_topic(topic_id: int):
    try:
        conn = sqlite3.connect("knowledge-base.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * from chunks where topic_id=?", (str(topic_id),))
        rows = cursor.fetchall()

        return rows

    except sqlite3.Error as e:
        print(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_topic_ids_for_unit(unit_id: int):
    try:
        conn = sqlite3.connect("knowledge-base.db")
        cursor = conn.cursor()

        cursor.execute(f"SELECT id from topics where unit_id={unit_id}")
        rows = cursor.fetchall()
        return rows

    except sqlite3.Error as e:
        print(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_subject_for_unit(unit_id: int):
    try:
        conn = sqlite3.connect("knowledge-base.db")
        cursor = conn.cursor()

        cursor.execute(
            """
        SELECT subjects.display_name
        FROM units
        JOIN subjects ON units.subject_id = subjects.id
        WHERE units.id = ?;
        """,
            (unit_id,),
        )
        rows = cursor.fetchall()
        return rows[0][0]

    except sqlite3.Error as e:
        print(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# MongoDB functions
def insert_doc(client, userId, subject):
    """
    Update the MongoDB collection with the provided data.
    """
    try:
        db = client["main"]
        collection = db["PPT"]
        time = datetime.now(pytz.timezone("Asia/Kolkata"))
        result = collection.insert_one(
            {
                "userId": userId,
                "start_time": time.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
                "name": subject,
                "status": "started",
                "error_msg": "None",
                "placeholders": [],
                "layouts": [],
            }
        )
        return str(result.inserted_id)
    except Exception as e:
        print(f"MongoDB Insert Error: {e}")


def update_placeholders(client, doc_id, placeholders, status, error_msg="None"):
    """
    Update the MongoDB collection with the provided data.
    """
    try:
        db = client["main"]
        collection = db["PPT"]
        time = datetime.now(pytz.timezone("Asia/Kolkata"))
        collection.update_one(
            {"_id": ObjectId(f"{doc_id}")},
            {
                "$set": {
                    "placeholders": placeholders,
                    "status": status,
                    "error_msg": error_msg,
                    "last_update": time.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
                }
            },
        )
    except Exception as e:
        print(f"MongoDB Update Error: {e}")


def update_layouts(client, doc_id, layouts, status, error_msg="None"):
    """
    Update the MongoDB collection with the provided data.
    """
    try:
        db = client["main"]
        collection = db["PPT"]
        time = datetime.now(pytz.timezone("Asia/Kolkata"))
        collection.update_one(
            {"_id": ObjectId(f"{doc_id}")},
            {
                "$set": {
                    "layouts": layouts,
                    "status": status,
                    "error_msg": error_msg,
                    "last_update": time.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
                }
            },
        )
    except Exception as e:
        print(f"MongoDB Update Error: {e}")


def final_update(client, doc_id, placeholders, status):
    """
    Update the MongoDB collection with the provided data.
    """
    try:
        db = client["main"]
        collection = db["PPT"]
        time = datetime.now(pytz.timezone("Asia/Kolkata"))
        collection.update_one(
            {"_id": ObjectId(f"{doc_id}")},
            {
                "$set": {
                    "placeholders": placeholders,
                    "status": status,
                    "finish_time": time.strftime("%Y-%m-%d %H:%M:%S %Z%z"),
                }
            },
        )
    except Exception as e:
        print(f"MongoDB Update Error: {e}")
