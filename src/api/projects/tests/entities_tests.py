import unittest

from src.api import create_api


class EntitiesTestCase(unittest.TestCase):
    def test_something(self):
        app = create_api()
        tester = app.test_client(self)
        resp = tester.get('/status', content_type='application/json')
        self.assertEqual(resp, {'ok'})


if __name__ == '__main__':
    unittest.main()
