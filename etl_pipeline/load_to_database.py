import sqlite3


DB_NAME = "chanchal_posts.db"


def load_data(posts, db_name=DB_NAME):
    connection = sqlite3.connect(db_name)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cb_posts (
                post_id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                status TEXT NOT NULL
                    CHECK (status IN ('lengthy', 'concise')),
                body_length INTEGER NOT NULL,
                user_name TEXT,
                user_email TEXT,
                company TEXT
            )
        """)

        cursor.executemany("""
            INSERT OR REPLACE INTO cb_posts (
                post_id, user_id, title, body, status,
                body_length, user_name, user_email, company
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                post["post_id"],
                post["user_id"],
                post["title"],
                post["body"],
                post["status"],
                post["body_length"],
                post["user_name"],
                post["user_email"],
                post["company"]
            )
            for post in posts
        ])

        connection.commit()
        print(f"Successfully loaded {len(posts)} posts into {db_name}.")

    finally:
        connection.close()
