import unittest

from src.api.funders.entities import Funder
from src.api.fundings.entities import Funding
from src.api.projects.entities import Project
from src.api.receipts.db_services import ReceiptDBService
from src.api.receipts.entities import Receipt, ReceiptSchema
from src.shared.test_base import DBBaseTestCase


class ReceiptDBServiceTestCase(DBBaseTestCase):
    def setUp(self):
        super(ReceiptDBServiceTestCase, self).setUp()
        self.db.session.execute("INSERT INTO public.financeur (id_financeur, nom_financeur, "
                                "ref_arret_attributif_financeur) VALUES (1, 'Jean Receipt Dupont', null)")
        self.db.session.execute("INSERT INTO public.projet (id_p, code_p, nom_p, statut_p, id_u) "
                                "VALUES (1, 'OC19', 'Receipt tests', true, 1)")
        self.db.session.execute("INSERT INTO public.financement (id_f, id_p, id_financeur, montant_arrete_f, "
                                "date_arrete_f, date_limite_solde_f,statut_f, date_solde_f, commentaire_admin_f, "
                                "commentaire_resp_f, numero_titre_f,annee_titre_f, imputation_f) "
                                "VALUES (1, 1, 1, 44344, null, null, 'ANTR', '2010-05-01', null, "
                                "null, null, null, null)")
        self.db.session.commit()

    def test_insert_receipt(self):
        receipt = Receipt(id_f=1, annee_r=2020, montant_r=699.3)
        receipt = ReceiptDBService.insert(receipt)

        self.assertEqual(receipt['id_f'], 1)
        self.assertEqual(receipt['annee_r'], 2020)
        self.assertEqual(receipt['montant_r'], 699.3)
        self.db.session.query(Receipt).filter_by(id_r=receipt['id_r']).delete()
        self.db.session.commit()

    def test_update_receipt(self):
        receipt = Receipt(id_f=1, annee_r=2020, montant_r=699.3)
        self.db.session.add(receipt)
        self.db.session.commit()

        receipt.annee_r = '2019'
        receipt.montant_r = '3093.19'
        updated_receipt = ReceiptDBService.update(receipt)

        self.assertEqual(updated_receipt['id_r'], receipt.id_r)
        self.assertEqual(updated_receipt['id_f'], 1)
        self.assertEqual(updated_receipt['annee_r'], 2019)
        self.assertEqual(updated_receipt['montant_r'], 3093.19)
        self.db.session.query(Receipt).filter_by(id_r=receipt.id_r).delete()
        self.db.session.commit()

    def test_check_receipt_exists_by_id(self):
        exists_not_found = ReceiptDBService.check_receipt_exists_by_id(13)
        self.assertEqual(exists_not_found['code'], 'RECEIPT_NOT_FOUND')

        receipt = Receipt(id_f=1, annee_r=2021, montant_r='3779')
        self.db.session.add(receipt)
        self.db.session.commit()
        receipt = ReceiptSchema().dump(receipt)

        exists_ok = ReceiptDBService.check_receipt_exists_by_id(receipt['id_r'])
        self.assertEqual(exists_ok, None)
        self.db.session.query(Receipt).filter_by(id_r=receipt['id_r']).delete()
        self.db.session.commit()

    def test_get_receipt_by_id(self):
        receipt = Receipt(id_f=1, annee_r=2018, montant_r='79')
        self.db.session.add(receipt)
        self.db.session.commit()
        receipt = ReceiptSchema().dump(receipt)

        receipt_found = ReceiptDBService.get_receipt_by_id(receipt['id_r'])
        self.assertEqual(receipt_found, receipt)
        self.db.session.query(Receipt).filter_by(id_r=receipt['id_r']).delete()
        self.db.session.commit()

    def test_get_receipts_by_funding_id(self):
        receipt = Receipt(id_f=1, annee_r=2021, montant_r=8784)
        self.db.session.add(receipt)
        self.db.session.commit()
        receipt = ReceiptSchema().dump(receipt)

        receipts_of_funding_1 = ReceiptDBService.get_receipts_by_funding_id(1)

        self.assertTrue('difference' in receipts_of_funding_1[0])
        self.db.session.query(Receipt).filter_by(id_r=receipt['id_r']).delete()
        self.db.session.commit()

    def test_is_project_solde(self):
        receipt = Receipt(id_f=1, annee_r=2020, montant_r=8784)
        self.db.session.add(receipt)
        self.db.session.commit()
        receipt = ReceiptSchema().dump(receipt)

        is_solde = ReceiptDBService.is_project_solde(receipt['id_r'])

        self.assertTrue(is_solde)
        self.db.session.query(Receipt).filter_by(id_r=receipt['id_r']).delete()
        self.db.session.commit()

    # TODO: test delete

    def tearDown(self):
        super(ReceiptDBServiceTestCase, self).tearDown()
        self.db.session.query(Funding).filter_by(id_f=1).delete()
        self.db.session.query(Funder).filter_by(id_financeur=1).delete()
        self.db.session.query(Project).filter_by(id_p=1).delete()
        self.db.session.commit()


if __name__ == '__main__':
    unittest.main()
