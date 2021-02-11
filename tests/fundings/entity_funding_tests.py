import unittest

from src.api.fundings.entities import Funding


class EntitiesTestCase(unittest.TestCase):
    def test_funding_entity(self):
        funding = Funding(1, 1, 10, 'ANTR')
        self.assertEqual(funding.id_p, 1)
        self.assertEqual(funding.id_financeur, 1)
        self.assertEqual(funding.montant_arrete_f, 10)
        self.assertEqual(funding.statut_f, 'ANTR')


if __name__ == '__main__':
    unittest.main()
