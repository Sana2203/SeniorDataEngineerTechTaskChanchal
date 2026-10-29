import unittest
from main import transform_data


class TestTransformData(unittest.TestCase):

    def setUp(self):
        self.posts = [
            {
                "userId": 1,
                "id": 1,
                "title": "Short title",
                "body": "a" * 150
            },
            {
                "userId": 2,
                "id": 2,
                "title": "Long title",
                "body": "b" * 151
            }
        ]

        self.users = [
            {
                "id": 1,
                "name": "User One",
                "email": "user1@example.com",
                "company": {"name": "Company One"}
            },
            {
                "id": 2,
                "name": "User Two",
                "email": "user2@example.com",
                "company": {"name": "Company Two"}
            }
        ]

    def test_post_status(self):
        result = transform_data(self.posts, self.users)
        self.assertEqual(result[0]["status"], "concise")
        self.assertEqual(result[1]["status"], "lengthy")

    def test_body_length(self):
        result = transform_data(self.posts, self.users)
        self.assertEqual(result[0]["body_length"], 150)
        self.assertEqual(result[1]["body_length"], 151)

    def test_user_details_are_joined(self):
        result = transform_data(self.posts, self.users)
        self.assertEqual(result[0]["user_name"], "User One")
        self.assertEqual(result[1]["user_name"], "User Two")
        self.assertEqual(result[0]["company"], "Company One")

    def test_post_count(self):
        result = transform_data(self.posts, self.users)
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()