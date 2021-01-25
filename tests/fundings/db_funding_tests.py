import unittest

from src.api.funders.entities import Funder
from src.api.fundings.db_services import FundingDBService
from src.api.fundings.entities import Funding
from src.api.projects.entities import Project
from src.shared.test_base import DBBaseTestCase


# Postgresql unittest example: https://github.com/axelcdv/flask-testing/


class DBServiceTestCase(DBBaseTestCase):
    def test_get_funding_by_project(self):
        funding = FundingDBService.get_funding_by_project(10)
        self.assertEqual(funding, [])

        new_project = Project(id_p=1, nom_p='auto test', code_p='210077', statut_p=True, id_u=1)
        self.db.session.add(new_project)

        new_funder = Funder(id_financeur=1, nom_financeur="Jean Dupont", ref_arret_attributif_financeur=None)
        new_funding = Funding(id_p=1, id_financeur=1, montant_arrete_f=10, statut_f='ANTR',
                              date_solde_f=None, date_arrete_f=None, date_limite_solde_f=None, commentaire_admin_f='',
                              commentaire_resp_f='', numero_titre_f='', annee_titre_f='', imputation_f='', )
        self.db.session.add(new_funder)
        self.db.session.add(new_funding)
        self.db.session.commit()
        fundings = FundingDBService.get_funding_by_project(new_funding.id_p)
        self.assertEqual(fundings[-1]['id_p'], new_funding.id_p)
        self.assertEqual(fundings[-1]['statut_f'], new_funding.statut_f)
        self.assertEqual(fundings[-1]['montant_arrete_f'], new_funding.montant_arrete_f)

    # TODO: test the other methods


if __name__ == '__main__':
    unittest.main()
