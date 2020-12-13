import unittest

from src.api import create_api
from src.api.status.resources import resources as status_ressources


class ResourceTestCase(unittest.TestCase):
    def test_status_resource(self):
        app = create_api()
        app.register_blueprint(status_ressources)

        tester = app.test_client(self)
        resp = tester.get('/status', content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, b'"ok"\n')


if __name__ == '__main__':
    unittest.main()
