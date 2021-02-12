import unittest

from src.api.funders.entities import Funder
from src.api.fundings.db_services import FundingDBService
from src.api.fundings.entities import Funding, FundingSchema
from src.api.projects.entities import Project
from src.shared.test_base import DBBaseTestCase


def insert_mock_data(db):
    new_project = Project(id_p=1, nom_p='auto test', code_p='210077', statut_p=True, id_u=1)
    db.session.add(new_project)

    new_funder = Funder(id_financeur=1, nom_financeur="Jean Dupont", ref_arret_attributif_financeur=None)
    new_funding = Funding(id_p=1, id_financeur=1, montant_arrete_f=10, statut_f='ANTR',
                          date_solde_f=None, date_arrete_f=None, date_limite_solde_f=None, commentaire_admin_f='',
                          commentaire_resp_f='', numero_titre_f='', annee_titre_f='', imputation_f='', )
    db.session.add(new_funder)
    db.session.add(new_funding)
    db.session.commit()
    return {
        'project': new_project,
        'funding': new_funding,
        'funder': new_funder,
    }


# Postgresql unittest example: https://github.com/axelcdv/flask-testing/
class DBServiceTestCase(DBBaseTestCase):
    def test_get_funding_by_project_empty(self):
        funding = FundingDBService.get_fundings_by_project(10)
        self.assertEqual(funding, [])

    def test_get_funding_by_project_ok(self):
        mock_data = insert_mock_data(self.db)
        new_funding = mock_data['funding']

        fundings = FundingDBService.get_fundings_by_project(new_funding.id_p)
        self.assertEqual(fundings[-1]['id_p'], new_funding.id_p)
        self.assertEqual(fundings[-1]['statut_f'], new_funding.statut_f)
        self.assertEqual(fundings[-1]['montant_arrete_f'], new_funding.montant_arrete_f)

    def test_get_funding_by_funder_ok_1(self):
        mock_data = insert_mock_data(self.db)
        funder = mock_data['funder']

        all_funding_found = FundingDBService.get_funding_by_funder(funder.id_financeur)
        self.assertEqual(all_funding_found[0]['id_financeur'],
                         funder.id_financeur, f"L'id financeur attendu est {funder.id_financeur}")
        self.assertEqual(all_funding_found[0]['statut_f'], 'ANTR', 'Le statut atendu est ANTR')

    def test_get_funding_by_funder_empty(self):
        funder = FundingDBService.get_funding_by_funder(1)
        self.assertEqual(funder, [])

    def test_check_project_not_have_funding_ok(self):
        funding = FundingDBService.check_project_not_have_funding(3)
        self.assertEqual(funding, None)

    def test_insert(self):
        insert_mock_data(self.db)

        funding = {'id_p': 1, 'id_financeur': 1, 'montant_arrete_f': 10, 'statut_f': 'ANTR',
                   'date_solde_f': None, 'date_arrete_f': None, 'date_limite_solde_f': None, 'commentaire_admin_f': '',
                   'commentaire_resp_f': '', 'numero_titre_f': '', 'annee_titre_f': '', 'imputation_f': ''}
        f = FundingDBService.insert(funding)

        funding_found = self.db.session.query(Funding).filter_by(id_f=f['id_f']).first()
        self.assertEqual(funding_found.id_p, 1, "L'id projet attendu est 1")
        self.assertEqual(funding_found.montant_arrete_f, 10, 'Le montant arreté attendu est 10')

    def test_update(self):
        mocked_data = insert_mock_data(self.db)
        funding = mocked_data['funding']
        funding.commentaire_admin_f = 'new comment'
        funding_object = FundingSchema().dump(funding)
        FundingDBService.update(funding_object)

        self.assertEqual(funding.commentaire_admin_f, 'new comment')

if __name__ == '__main__':
    unittest.main()
