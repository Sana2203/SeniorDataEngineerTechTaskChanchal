from api_client import fetch_posts, fetch_users
from transform_data import transform_data
from load_to_database import load_data


def main():
    print("ETL Job Started")

    posts = fetch_posts()
    users = fetch_users()

    print(f"Posts fetched: {len(posts)}")
    print(f"Users fetched: {len(users)}")

    transformed_posts = transform_data(posts, users)
    print(f"Posts transformed: {len(transformed_posts)}")

    load_data(transformed_posts)

    print("ETL Job Finished")


if __name__ == "__main__":
    main()
