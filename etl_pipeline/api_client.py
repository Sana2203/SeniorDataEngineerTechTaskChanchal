import json
import urllib.request


BASE_URL = "https://jsonplaceholder.typicode.com"


def fetch_posts():
    return _fetch_json(f"{BASE_URL}/posts")


def fetch_users():
    return _fetch_json(f"{BASE_URL}/users")


def _fetch_json(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "SeniorDataEngineerETL/1.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))
