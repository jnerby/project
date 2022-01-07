import unittest
from server import app
from model import connect_to_db, db

class FlaskTests(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        #### use testdb to seed db
        connect_to_db(app, "postgresql:///testdb")

        # Test as logged in user
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    # def test_login(self):
    #     """Test login page."""
    #     result = self.client.post("/login",
    #                               data={"username": "testuser", "password": "testuserpw"},
    #                               follow_redirects=True)
    #     self.assertIn(b"Welcome!", result.data)

    def test_homepage(self):
        """Test home page"""
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Profile', result.data)
        # self.assertIn(b'Notifications', result.data)


#   def tearDown(self):
#       """Stuff to do after each test."""

if __name__ == "__main__":
    unittest.main()