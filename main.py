import urllib.request
import json
import sqlite3


POSTS_URL = "https://jsonplaceholder.typicode.com/posts"
USERS_URL = "https://jsonplaceholder.typicode.com/users"
DB_NAME = "chanchal_posts.db"


def fetch_data(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def transform_data(posts, users):
    users_by_id = {user["id"]: user for user in users}
    transformed_posts = []

    for post in posts:
        user = users_by_id.get(post["userId"], {})

        body = post.get("body", "")
        title = post.get("title", "")

        transformed_posts.append({
            "post_id": post["id"],
            "user_id": post["userId"],
            "title": title,
            "body": body,
            "status": "lengthy" if len(body) > 150 else "concise",
            "body_length": len(body),
            "user_name": user.get("name", ""),
            "user_email": user.get("email", ""),
            "company": user.get("company", {}).get("name", "")
        })

    return transformed_posts


def load_data(posts):
    connection = sqlite3.connect(DB_NAME)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cb_posts (
                post_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                title TEXT,
                body TEXT,
                status TEXT,
                body_length INTEGER,
                user_name TEXT,
                user_email TEXT,
                company TEXT
            )
        """)

        cursor.executemany("""
            INSERT OR REPLACE INTO cb_posts
            (post_id, user_id, title, body, status, body_length,
             user_name, user_email, company)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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

        cursor.execute("SELECT COUNT(*) FROM cb_posts")
        count = cursor.fetchone()[0]

        print("Data loaded successfully!")
        print("Total records in database:", count)
        print("Database file:", DB_NAME)

    finally:
        connection.close()


def main():
    print("Fetching posts and users...")

    posts = fetch_data(POSTS_URL)
    users = fetch_data(USERS_URL)

    print("Posts fetched:", len(posts))
    print("Users fetched:", len(users))

    transformed_posts = transform_data(posts, users)

    print("Posts transformed:", len(transformed_posts))

    load_data(transformed_posts)


if __name__ == "__main__":
    main()