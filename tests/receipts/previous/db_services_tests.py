import unittest

from src.api.receipts.previous.db_services import InputOutputDBService
from src.api.receipts.previous.entities import InputOutput, InputOutputSchema
from src.shared.test_base import DBBaseTestCase


class InputOutputDBServiceTestCase(DBBaseTestCase):
    def setUp(self):
        super(InputOutputDBServiceTestCase, self).setUp()

        self.db.session.execute("INSERT INTO public.entree_sortie (annee_recette_es, annee_affectation_es, "
                                "montant_es) VALUES (2020, 2022, 122.5)")
        self.db.session.execute("INSERT INTO public.entree_sortie (annee_recette_es, annee_affectation_es, "
                                "montant_es) VALUES (2020, 2023, 123.5)")
        self.db.session.execute("INSERT INTO public.entree_sortie (annee_recette_es, annee_affectation_es, "
                                "montant_es) VALUES (2020, 2024, 124.5)")
        self.db.session.commit()

    def test_insert_input_output(self):
        input_output = InputOutput(annee_recette_es=2020, annee_affectation_es=2025, montant_es=699.3)
        input_output = InputOutputDBService.insert(input_output)

        self.assertEqual(input_output['annee_recette_es'], 2020)
        self.assertEqual(input_output['annee_affectation_es'], 2025)
        self.assertEqual(input_output['montant_es'], 699.3)
        self.db.session.query(InputOutput).filter_by(id_es=input_output['id_es']).delete()
        self.db.session.commit()

    def test_update_input_output(self):
        input_output = InputOutput(annee_recette_es=2020, annee_affectation_es=2025, montant_es=699.3)
        self.db.session.add(input_output)
        self.db.session.commit()

        input_output.annee_recette_es = 2021
        input_output.annee_affectation_es = 2080
        input_output.montant_es = 3093.19
        input_output_object = input_output
        print(input_output_object)
        updated_input_output = InputOutputDBService.update(input_output_object)

        self.assertEqual(updated_input_output['annee_recette_es'], 2021)
        self.assertEqual(updated_input_output['annee_affectation_es'], 2080)
        self.assertEqual(updated_input_output['montant_es'], 3093.19)
        self.db.session.commit()

    def test_get_input_output_by_id(self):
        input_output = InputOutput(annee_recette_es=2022, annee_affectation_es=2027, montant_es=3093.19)
        self.db.session.add(input_output)
        self.db.session.commit()
        input_output = InputOutputSchema().dump(input_output)

        input_output_found = InputOutputDBService.get_input_output_by_id(input_output['id_es'])
        self.assertEqual(input_output_found, input_output)
        self.db.session.query(InputOutput).filter_by(id_es=input_output['id_es']).delete()
        self.db.session.commit()

    def test_get_all_input_output(self):
        input_outputs = [InputOutput(annee_recette_es=2020, annee_affectation_es=2022, montant_es=122.5),
                         InputOutput(annee_recette_es=2020, annee_affectation_es=2023, montant_es=123.5),
                         InputOutput(annee_recette_es=2020, annee_affectation_es=2024, montant_es=124.5)]

        db_input_outputs = InputOutputDBService.get_input_output_by_filter()  # No Filters

        for test, actual in zip(input_outputs, db_input_outputs):
            self.assertEqual(actual['annee_recette_es'], test.annee_recette_es)
            self.assertEqual(actual['annee_affectation_es'], test.annee_affectation_es)
            self.assertEqual(actual['montant_es'], test.montant_es)

    def tearDown(self):
        super(InputOutputDBServiceTestCase, self).tearDown()
        self.db.session.execute("DELETE FROM entree_sortie")
        self.db.session.commit()


if __name__ == '__main__':
    unittest.main()
