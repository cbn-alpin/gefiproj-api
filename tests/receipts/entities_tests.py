import unittest

from src.api.receipts.entities import Receipt, ReceiptSchema


class Entities(unittest.TestCase):
    def test_receipt_entity(self):
        receipt = Receipt(id_f=2, montant_r=290.6, annee_r=2019)
        self.assertEqual(receipt.id_r, None)
        self.assertEqual(receipt.id_f, 2)
        self.assertEqual(receipt.montant_r, 290.6)
        self.assertEqual(receipt.annee_r, 2019)

    def test_receipt_schema(self):
        receipt_data = ReceiptSchema().load({'id_f': 3, 'montant_r': '499', 'annee_r': 2018})
        receipt = Receipt(**receipt_data)

        self.assertEqual(receipt.id_f, 3)
        self.assertEqual(receipt.annee_r, 2018)
        self.assertEqual(receipt.montant_r, 499)


if __name__ == '__main__':
    unittest.main()
