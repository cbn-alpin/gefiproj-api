import unittest

from flask_sqlalchemy import SQLAlchemy

from src.api import create_api
from src.api.funders.entities import Funder
from src.api.fundings.entities import Funding
from src.api.projects.entities import Project
from src.api.receipts.entities import Receipt
from src.api.receipts.resources import resources
from src.shared import config

TEST_TOKEN = config.get_test_token()
BASE_URL = '/api/receipts'
CONTENT_TYPE = 'application/json'


class RessourceTestCase(unittest.TestCase):

    def clean_db(self):
        for table in [Receipt, Funding, Project, Funder]:
            self.db.session.query(table).delete()
        self.db.session.commit()

    def setUp(self):
        self.app = create_api('test')
        self.db = SQLAlchemy()
        self.db.app = self.app
        self.app.register_blueprint(resources)
        self.tester = self.app.test_client(self)

        self.clean_db()
        self.db.session.execute("INSERT INTO public.financeur (id_financeur, nom_financeur, "
                                "ref_arret_attributif_financeur) VALUES (1, 'Jean Receipt Dupont', null)")
        self.db.session.execute("INSERT INTO public.projet (id_p, code_p, nom_p, statut_p, id_u) "
                                "VALUES (1, 210009, 'Receipt tests', true, 1)")
        self.db.session.execute("INSERT INTO public.financement (id_f, id_p, id_financeur, montant_arrete_f, "
                                "date_arrete_f, date_limite_solde_f,statut_f, date_solde_f, commentaire_admin_f, "
                                "commentaire_resp_f, numero_titre_f,annee_titre_f, imputation_f) "
                                "VALUES (1, 1, 1, 44344, null, null, 'ANTR', '2010-05-01', null, "
                                "null, null, null, null)")
        self.db.session.execute("INSERT INTO public.recette (id_r, id_f, montant_r, annee_r) "
                                "VALUES (10, 1, 307.3, 2019)")
        self.db.session.commit()

    def test_add_receipt_invalid_data(self):
        receipt_data = {
            "annee_r": "2021",
            "montant_r": 309.38,
        }

        resp422 = self.tester.post(BASE_URL,
                                   headers={'content_type': CONTENT_TYPE,
                                            'Authorization': f'Bearer {TEST_TOKEN}'},
                                   json=receipt_data)

        self.assertEqual(resp422.status_code, 422)

    def test_add_receipt_400(self):
        receipt_data_1 = Receipt(1, 303, 2020)
        self.db.session.add(receipt_data_1)
        self.db.session.commit()

        receipt_data = {
            "annee_r": "2020",
            "montant_r": 719.21,
            "id_f": 1
        }

        resp400 = self.tester.post(BASE_URL,
                                   headers={'content_type': CONTENT_TYPE,
                                            'Authorization': f'Bearer {TEST_TOKEN}'},
                                   json=receipt_data)

        self.assertEqual(resp400.status_code, 400)
        self.db.session.query(Receipt).filter_by(id_r=receipt_data_1.id_r).delete()
        self.db.session.commit()

    def test_add_receipt_ok(self):
        receipt_data = {
            "annee_r": "2020",
            "montant_r": 719.21,
            "id_f": 1
        }

        resp200 = self.tester.post(BASE_URL,
                                   headers={'content_type': CONTENT_TYPE,
                                            'Authorization': f'Bearer {TEST_TOKEN}'},
                                   json=receipt_data)
        response_json = resp200.get_json()

        self.assertEqual(resp200.status_code, 200)
        self.assertEqual(response_json['annee_r'], 2020)
        self.assertEqual(response_json['montant_r'], 719.21)
        self.assertEqual(response_json['id_f'], 1)
        self.assertFalse(response_json['id_r'] is None)

    def test_update_not_found_receipt(self):
        receipt_data = {
            "annee_r": "2020",
            "montant_r": 307.21,
            "id_f": 1
        }

        resp404 = self.tester.put(BASE_URL + '/11',
                                  headers={'content_type': CONTENT_TYPE,
                                           'Authorization': f'Bearer {TEST_TOKEN}'},
                                  json=receipt_data)
        self.assertEqual(resp404.status_code, 404)

    def test_update_receipt_invalid_data(self):
        receipt_data = {
            "annee_r": "2021",
            "montant_r": 307.21,
        }

        resp422 = self.tester.put(BASE_URL + '/10',
                                  headers={'content_type': CONTENT_TYPE,
                                           'Authorization': f'Bearer {TEST_TOKEN}'},
                                  json=receipt_data)

        self.assertEqual(resp422.status_code, 422)

    def test_update_receipt_ok(self):
        receipt_data = {
            "annee_r": "2021",
            "montant_r": 307.21,
            "id_f": 1
        }

        resp200 = self.tester.put(BASE_URL + '/10',
                                  headers={'content_type': CONTENT_TYPE,
                                           'Authorization': f'Bearer {TEST_TOKEN}'},
                                  json=receipt_data)
        response_json = resp200.get_json()
        self.assertEqual(resp200.status_code, 200)
        self.assertEqual(response_json['annee_r'], 2021)
        self.assertEqual(response_json['montant_r'], 307.21)
        self.assertEqual(response_json['id_f'], 1)
        self.assertEqual(response_json['id_r'], 10)

    def test_update_receipt_funding_fail(self):
        receipt_data = {
            "annee_r": "2020",
            "montant_r": 307.21,
            "id_f": 2
        }
        resp400 = self.tester.put(BASE_URL + '/10',
                                  headers={'content_type': CONTENT_TYPE,
                                           'Authorization': f'Bearer {TEST_TOKEN}'},
                                  json=receipt_data)
        self.assertEqual(resp400.status_code, 400)

    def tearDown(self):
        self.clean_db()


if __name__ == '__main__':
    unittest.main()
