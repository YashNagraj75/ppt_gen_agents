import sqlite3


def get_topics_for_unit(unit_id: int):
    try:
        conn = sqlite3.connect("knowledge-base.db")
        cursor = conn.cursor()

        cursor.execute(f"SELECT * from topics where unit_id={unit_id}")
        rows = cursor.fetchall()
        return rows

    except sqlite3.Error as e:
        print(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
