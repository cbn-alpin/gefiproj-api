import unittest

from src.api import create_api
from src.api.projects.resources import resources
from src.shared import config

# REST API test example https://dev.to/paurakhsharma/flask-rest-api-part-6-testing-rest-apis-4lla

TEST_TOKEN = config.get_test_token()


class RessourceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_api('test')
        self.app.register_blueprint(resources)
        self.tester = self.app.test_client(self)

    def test_token(self):
        # no token test
        resp401 = self.tester.get('/api/projects', headers={'content_type': 'application/json'})
        self.assertEqual(resp401.status_code, 401)

        # invalid token test
        resp422 = self.tester.get('/api/projects',
                                  headers={'content_type': 'application/json', 'Authorization': f'{TEST_TOKEN}'})
        self.assertEqual(resp422.status_code, 422)

        # valid token test
        resp200 = self.tester.get('/api/projects',
                                  headers={'content_type': 'application/json', 'Authorization': f'Bearer {TEST_TOKEN}'})
        self.assertEqual(resp200.status_code, 200)

    def test_get_all_projects_resource(self):
        resp = self.tester.get('/api/projects',
                               headers={'content_type': 'application/json', 'Authorization': f'Bearer {TEST_TOKEN}'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), 0)


if __name__ == '__main__':
    unittest.main()
