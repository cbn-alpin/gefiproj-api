import unittest

from src.api.receipts.previous.entities import InputOutput, InputOutputSchema


class Entities(unittest.TestCase):
    def test_input_output_entity(self):
        inout_output = InputOutput(annee_recette_es=2027, annee_affectation_es=2050, montant_es=2654.6)
        self.assertEqual(inout_output.id_es, None)
        self.assertEqual(inout_output.annee_recette_es, 2027)
        self.assertEqual(inout_output.annee_affectation_es, 2050)
        self.assertEqual(inout_output.montant_es, 2654.6)

    def test_input_output_schema(self):
        input_output_data = InputOutputSchema().load(
            {'annee_recette_es': 2027, 'annee_affectation_es': 2050, 'montant_es': 2654.6})
        inout_output = InputOutput(**input_output_data)

        self.assertEqual(inout_output.annee_recette_es, 2027)
        self.assertEqual(inout_output.annee_affectation_es, 2050)
        self.assertEqual(inout_output.montant_es, 2654.6)


if __name__ == '__main__':
    unittest.main()
