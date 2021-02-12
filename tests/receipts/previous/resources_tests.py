import unittest

from flask_sqlalchemy import SQLAlchemy

from src.api import create_api
from src.api.receipts.previous.entities import InputOutput
from src.api.receipts.previous.resources import resources
from src.shared import config

TEST_TOKEN = config.get_test_token()
BASE_URL = '/api/receipts/previous'
CONTENT_TYPE = 'application/json'


class RessourceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_api('test')
        self.db = SQLAlchemy()
        self.db.app = self.app
        self.app.register_blueprint(resources)
        self.tester = self.app.test_client(self)

        self.db.session.execute("DELETE FROM entree_sortie")
        self.db.session.commit()
        self.db.session.execute("INSERT INTO public.entree_sortie (annee_recette_es, annee_affectation_es, "
                                "montant_es) VALUES (2020, 2022, 122.5)")
        self.db.session.execute("INSERT INTO public.entree_sortie (annee_recette_es, annee_affectation_es, "
                                "montant_es) VALUES (2020, 2023, 123.5)")
        self.db.session.execute("INSERT INTO public.entree_sortie (annee_recette_es, annee_affectation_es, "
                                "montant_es) VALUES (2020, 2024, 124.5)")
        self.db.session.commit()

    def test_get_all_input_output(self):
        input_outputs = [InputOutput(annee_recette_es=2020, annee_affectation_es=2022, montant_es=122.5),
                         InputOutput(annee_recette_es=2020, annee_affectation_es=2023, montant_es=123.5),
                         InputOutput(annee_recette_es=2020, annee_affectation_es=2024, montant_es=124.5)]

        resp200 = self.tester.get(BASE_URL,
                                  headers={'content_type': CONTENT_TYPE,
                                           'Authorization': f'Bearer {TEST_TOKEN}'})
        input_output_json = resp200.get_json()

        for test, actual in zip(input_outputs, input_output_json):
            self.assertEqual(actual['annee_recette_es'], test.annee_recette_es)
            self.assertEqual(actual['annee_affectation_es'], test.annee_affectation_es)
            self.assertEqual(actual['montant_es'], test.montant_es)

    def test_add_input_output_invalid_data(self):
        input_output_data = {
            "annee_recette_es": "2021",
            "annee_affectation_es": 2066,
            "montant_es": 309.38
        }

        resp422 = self.tester.post(BASE_URL,
                                   headers={'content_type': CONTENT_TYPE,
                                            'Authorization': f'Bearer {TEST_TOKEN}'},
                                   json=input_output_data)

        self.assertEqual(resp422.status_code, 422)

    def test_add_input_output_ok(self):
        input_output_data = {
            "annee_recette_es": 2021,
            "annee_affectation_es": 2066,
            "montant_es": 309.38
        }

        resp200 = self.tester.post(BASE_URL,
                                   headers={'content_type': CONTENT_TYPE,
                                            'Authorization': f'Bearer {TEST_TOKEN}'},
                                   json=input_output_data)
        response_json = resp200.get_json()

        self.assertEqual(resp200.status_code, 201)
        self.assertEqual(response_json['annee_recette_es'], 2021)
        self.assertEqual(response_json['annee_affectation_es'], 2066)
        self.assertEqual(response_json['montant_es'], 309.38)
        self.assertFalse(response_json['id_es'] is None)

    def test_update_input_output_invalid_data(self):
        input_output_data = {
            "annee_recette_es": 2021,
            "annee_affectation_es": "2066",
            "montant_es": 309.38
        }

        resp422 = self.tester.put(BASE_URL + '/1',
                                  headers={'content_type': CONTENT_TYPE,
                                           'Authorization': f'Bearer {TEST_TOKEN}'},
                                  json=input_output_data)

        self.assertEqual(resp422.status_code, 422)

    def test_update_input_output_ok(self):
        input_output_data = {
            "annee_recette_es": 2021,
            "annee_affectation_es": 2066,
            "montant_es": 309.38
        }

        resp200 = self.tester.get(BASE_URL,
                                  headers={'content_type': CONTENT_TYPE,
                                           'Authorization': f'Bearer {TEST_TOKEN}'})
        id = resp200.get_json()[0]['id_es']

        resp200 = self.tester.put(BASE_URL + '/' + str(id),
                                  headers={'content_type': CONTENT_TYPE,
                                           'Authorization': f'Bearer {TEST_TOKEN}'},
                                  json=input_output_data)
        response_json = resp200.get_json()
        self.assertEqual(resp200.status_code, 200)
        self.assertEqual(response_json['annee_recette_es'], 2021)
        self.assertEqual(response_json['annee_affectation_es'], 2066)
        self.assertEqual(response_json['montant_es'], 309.38)
        self.assertEqual(response_json['id_es'], id)

    def tearDown(self):
        self.db.session.execute("DELETE FROM entree_sortie")
        self.db.session.commit()

    if __name__ == '__main__':
        unittest.main()
