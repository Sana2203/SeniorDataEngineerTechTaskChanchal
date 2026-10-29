def transform_data(posts, users):
    users_by_id = {user["id"]: user for user in users}
    transformed_posts = []

    for post in posts:
        user = users_by_id.get(post["userId"], {})
        title = post.get("title", "")
        body = post.get("body", "")

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
