import unittest
from server import app
from model import connect_to_db, db

class FlaskTests(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database, seeded from testdb.sql
        connect_to_db(app, "postgresql:///testdb")

        # Test as logged in user
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_login(self):
        """Test Login page."""
        result = self.client.post("/login",
                                  data={"login-username": "dragonmum", "login-password": "dragonmum"},
                                  follow_redirects=True)
        self.assertIn(b"Welcome!", result.data)

    def test_homepage(self):
        """Test home page (WatchList button in nav bar)"""
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Profile', result.data)
        self.assertIn(b'notifications', result.data)

    def test_my_lists(self):
        """Test MyLists page"""
        result = self.client.get("/mylists")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'WatchLists', result.data)

    def test_search(self):
        """Test Search page"""
        result = self.client.get("/search")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Search', result.data)
        self.assertIn(b'history', result.data)
        self.assertIn(b'<img', result.data)


    def test_history(self):
        """Test History page"""
        result = self.client.get("/history")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Watchlist History', result.data)

    def test_clubs(self):
        """Test Clubs page"""
        result = self.client.get("/clubs")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Start a Club', result.data)
        self.assertIn(b'Owner', result.data)

    def test_logout(self):
        """Test Logout page."""
        result = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Login', result.data)


if __name__ == "__main__":
    unittest.main()