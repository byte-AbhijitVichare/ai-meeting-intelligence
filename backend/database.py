import sqlite3


def create_database():

    conn = sqlite3.connect(
        "database/meetings.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meetings (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        transcript TEXT,

        summary TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()

    conn.close()

def save_meeting(
    filename,
    transcript,
    summary
):

    conn = sqlite3.connect(
        "database/meetings.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO meetings
        (
            filename,
            transcript,
            summary
        )
        VALUES (?, ?, ?)
        """,
        (
            filename,
            transcript,
            summary
        )
    )

    conn.commit()

    conn.close()

def get_meetings():

    conn = sqlite3.connect(
        "database/meetings.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            filename,
            created_at
        FROM meetings
        ORDER BY id DESC
        """
    )

    meetings = cursor.fetchall()

    conn.close()

    return meetings

def get_meeting_by_id(meeting_id):

    conn = sqlite3.connect(
        "database/meetings.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            filename,
            transcript,
            summary
        FROM meetings
        WHERE id = ?
        """,
        (meeting_id,)
    )

    meeting = cursor.fetchone()

    conn.close()

    return meeting

def search_meetings(keyword):

    conn = sqlite3.connect(
        "database/meetings.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            filename,
            created_at
        FROM meetings
        WHERE transcript LIKE ?
        OR summary LIKE ?
        ORDER BY id DESC
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )

    results = cursor.fetchall()

    conn.close()

    return results