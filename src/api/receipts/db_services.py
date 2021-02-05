from src.shared.entity import Session
from .entities import Receipt, ReceiptSchema, InputOutput, InputOutputSchema
from ..fundings.entities import Funding
from ..projects.entities import Project


class ReceiptDBService:
    @staticmethod
    def check_funding_exists(funding_id):
        session = Session()
        existing_funding = session.query(Funding).filter_by(id_f=funding_id).first()
        session.close()
        if existing_funding is None:
            raise ValueError(f'Le financement {funding_id} n\'existe pas.', 404)

    @staticmethod
    def get_receipts_of_year_by_funding_id(funding_id: int or str, year: int or str):
        session = None
        receipts = None

        try:
            session = Session()
            receipts = session.query(Receipt).filter(Receipt.id_f == funding_id, Receipt.annee_r == year).all()
            receipts = ReceiptSchema(many=True).dump(receipts)
        finally:
            session.close()

        return receipts

    @staticmethod
    def get_receipts_by_funding_id(funding_id: int):
        session = Session()
        receipt_object = session.query(Receipt).filter_by(id_f=funding_id).order_by(Receipt.id_r).all()

        rest_receipt_amount_object = session.execute("select r.id_r, (r.montant_r - sum(ma.montant_ma)) as difference "
                                                     "from recette r left join montant_affecte ma on ma.id_r = r.id_r "
                                                     "where r.id_f=:funding_id group by r.id_r order by r.id_r",
                                                     {'funding_id': funding_id})
        # https://stackoverflow.com/a/22084672
        rest_amounts = []
        for r in rest_receipt_amount_object:
            rest_amounts.append({'difference': r['difference'], 'id_r': r['id_r']})

        # Transforming into JSON-serializable objects
        schema = ReceiptSchema(many=True)
        receipts = schema.dump(receipt_object)
        if len(rest_amounts) > 0:
            for i, receipt in enumerate(receipts, start=0):
                receipt['difference'] = rest_amounts[i]['difference']

        session.close()
        return receipts

    @staticmethod
    def get_receipt_by_id(receipt_id: int):
        session = Session()
        receipt_object = session.query(Receipt).filter_by(id_r=receipt_id).first()

        schema = ReceiptSchema()
        receipt = schema.dump(receipt_object)
        session.close()

        return receipt

    @staticmethod
    def insert(receipt: Receipt):
        session = Session()
        session.add(receipt)
        session.commit()

        inserted_receipt = ReceiptSchema().dump(receipt)
        session.close()
        return inserted_receipt

    @staticmethod
    def update(receipt: Receipt):
        session = Session()
        session.merge(receipt)
        session.commit()

        updated_receipt = ReceiptSchema().dump(receipt)
        session.close()
        return updated_receipt

    @staticmethod
    def delete(receipt_id: int) -> int:
        session = Session()
        session.query(Receipt).filter_by(id_r=receipt_id).delete()
        session.commit()
        session.close()

        return receipt_id

    @staticmethod
    def check_receipt_exists_by_id(receipt_id: int):
        existing_receipt = ReceiptDBService.get_receipt_by_id(receipt_id)
        if not existing_receipt:
            msg = {
                'code': 'RECEIPT_NOT_FOUND',
                'message': f'Receipt with id <{receipt_id}> does not exist.'
            }

            return msg

    @staticmethod
    def is_project_solde(id_receipt):
        session = None
        try:
            session = Session()
            receipt_project_object = session.query(Receipt.id_r) \
                .join(Funding, Funding.id_f == Receipt.id_f) \
                .join(Project, Project.id_p == Funding.id_p) \
                .add_columns(Project.statut_p) \
                .filter(Receipt.id_r == id_receipt).first()

            return len(receipt_project_object) > 1 and receipt_project_object[1] is True
        except:
            return False
        finally:
            session.close()

class InputOutputDBService:
    @staticmethod
    def check_input_output_exists(input_output_id):
        existing_input_output=None
        session = Session()
        existing_input_output = session.query(InputOutput).filter_by(id_es=input_output_id).first()
        session.close()
        return existing_input_output


    @staticmethod
    def check_input_output_uniqueness(annee_recette, annee_affectation):
        existing_input_output=None
        session = Session()
        existing_input_output = session.query(InputOutput).filter_by(annee_recette_es=annee_recette, annee_affectation_es=annee_affectation).first()
        session.close()
        return existing_input_output


    @staticmethod
    def get_input_output_by_id(input_output_id: int):
        session = Session()
        input_output_object = session.query(InputOutput).filter_by(id_es=input_output_id).first()

        schema = InputOutputSchema()
        input_output = schema.dump(input_output_object)
        session.close()

        return input_output

    @staticmethod
    def get_input_output_by_filter(query_param=None):
        session = None
        input_outputs = None
        try:
            session = Session()
            input_outputs = session.query(InputOutput)

            if query_param is not None:
                annee_recette_es = query_param.get('annee_recette_es', default = None, type = int)
                if annee_recette_es is not None:
                    input_outputs = input_outputs.filter(InputOutput.annee_recette_es == annee_recette_es)

                annee_recette_es_sup = query_param.get('annee_recette_es_sup', default = None, type = int)
                if annee_recette_es_sup is not None:
                    input_outputs = input_outputs.filter(InputOutput.annee_recette_es >= annee_recette_es_sup)

                annee_recette_es_inf = query_param.get('annee_recette_es_inf', default = None, type = int)
                if annee_recette_es_inf is not None:
                    input_outputs = input_outputs.filter(InputOutput.annee_recette_es <= annee_recette_es_inf)

                annee_affectation_es = query_param.get('annee_affectation_es', default = None, type = int)
                if annee_affectation_es is not None:
                    input_outputs = input_outputs.filter(InputOutput.annee_affectation_es == annee_affectation_es)

                annee_affectation_es_sup = query_param.get('annee_affectation_es_sup', default = None, type = int)
                if annee_affectation_es_sup is not None:
                    input_outputs = input_outputs.filter(InputOutput.annee_affectation_es >= annee_affectation_es_sup)

                annee_affectation_es_inf = query_param.get('annee_affectation_es_inf', default = None, type = int)
                if annee_affectation_es_inf is not None:
                    input_outputs = input_outputs.filter(InputOutput.annee_affectation_es <= annee_affectation_es_inf)

                montant_es = query_param.get('montant_es', default = None, type = float)
                if montant_es is not None:
                    input_outputs = input_outputs.filter(InputOutput.montant_es == montant_es)

                montant_es_sup = query_param.get('montant_es_sup', default = None, type = float)
                if montant_es_sup is not None:
                    input_outputs = input_outputs.filter(InputOutput.montant_es >= montant_es_sup)

                montant_es_inf = query_param.get('montant_es_inf', default = None, type = float)
                if montant_es_inf is not None:
                    input_outputs = input_outputs.filter(InputOutput.montant_es <= montant_es_inf)

            input_outputs = input_outputs.all()
            input_outputs = InputOutputSchema(many=True).dump(input_outputs)
        finally:
            session.close()

        return input_outputs

    @staticmethod
    def insert(input_output: InputOutput):
        session = Session()
        session.add(input_output)
        session.commit()

        inserted_input_output = InputOutputSchema().dump(input_output)
        session.close()
        return inserted_input_output

    @staticmethod
    def update(input_output: InputOutput):
        session = Session()
        session.merge(input_output)
        session.commit()

        updated_input_output = InputOutputSchema().dump(input_output)
        session.close()
        return updated_input_output

    @staticmethod
    def delete(input_output_id: int) -> int:
        session = Session()
        session.query(InputOutput).filter_by(id_es=input_output_id).delete()
        session.commit()
        session.close()

        return input_output_id
