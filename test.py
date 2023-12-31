from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """set up for every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """double check the homepage"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_is_valid_word(self):
        """test if the word is on this board"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["T", "E", "S", "T", "T"], 
                                 ["T", "E", "S", "T", "T"], 
                                 ["T", "E", "S", "T", "T"], 
                                 ["T", "E", "S", "T", "T"], 
                                 ["T", "E", "S", "T", "T"]]
        response = self.client.get('/check-word?word=test')
        self.assertEqual(response.json['result'], 'ok')

    def test_not_on_board(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_a_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=abcdefghijklmnopqrstuvwxyz')
        self.assertEqual(response.json['result'], 'not-word')