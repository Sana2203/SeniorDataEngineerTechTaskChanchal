import sqlite3

connection = sqlite3.connect("chanchal_posts.db")

queries = {
    "Top 5 users with longest posts": """
        SELECT user_id, user_name, MAX(body_length) AS longest_post_length
        FROM cb_posts
        GROUP BY user_id, user_name
        ORDER BY longest_post_length DESC
        LIMIT 5
    """,

    "Average post length including title for top 5 users": """
        WITH top_users AS (
            SELECT user_id, user_name, MAX(body_length) AS longest_post_length
            FROM cb_posts
            GROUP BY user_id, user_name
            ORDER BY longest_post_length DESC
            LIMIT 5
        )
        SELECT p.user_id, p.user_name,
               ROUND(AVG(LENGTH(p.title) + LENGTH(p.body)), 2)
               AS average_post_length
        FROM cb_posts p
        JOIN top_users t ON p.user_id = t.user_id
        GROUP BY p.user_id, p.user_name
        ORDER BY average_post_length DESC
    """,

    "Weekday with most lengthy posts": """
        SELECT
            CASE strftime('%w', date('1970-01-01', '+' || post_id || ' days'))
                WHEN '0' THEN 'Sunday'
                WHEN '1' THEN 'Monday'
                WHEN '2' THEN 'Tuesday'
                WHEN '3' THEN 'Wednesday'
                WHEN '4' THEN 'Thursday'
                WHEN '5' THEN 'Friday'
                WHEN '6' THEN 'Saturday'
            END AS weekday,
            COUNT(*) AS lengthy_post_count
        FROM cb_posts
        WHERE status = 'lengthy'
        GROUP BY weekday
        ORDER BY lengthy_post_count DESC
        LIMIT 1
    """
}

try:
    for title, query in queries.items():
        print("\n" + "=" * 50)
        print(title)
        print("=" * 50)

        cursor = connection.execute(query)

        for row in cursor.fetchall():
            print(row)

finally:
    connection.close()