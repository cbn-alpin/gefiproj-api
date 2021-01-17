from src.shared.entity import Session
from .entities import Receipt, ReceiptSchema
from ..fundings.entities import Funding


class ReceiptDBService:
    @staticmethod
    def check_funding_exists(funding_id):
        session = Session()
        existing_funding = session.query(Funding).filter_by(id_f=funding_id).first()
        session.close()
        if existing_funding is None:
            raise ValueError(f'Le financement {funding_id} n\'existe pas.', 404)

    @staticmethod
    def get_receipts_by_funding_id(funding_id: int):
        session = Session()
        receipt_object = session.query(Receipt).filter_by(id_f=funding_id).order_by(Receipt.id_r).all()

        rest_receipt_amount_object = session.execute("select r.id_r, (r.montant_r - sum(ma.montant_ma)) as difference "
                                                     "from recette r left join montant_affecte ma on ma.id_r = r.id_r "
                                                     "where r.id_f=:funding_id group by r.id_r order by r.id_r",
                                                     {'funding_id': 1})
        # https://stackoverflow.com/a/22084672
        rest_amounts = []
        for r in rest_receipt_amount_object:
            print({'difference': r['difference'], 'id_r': r['id_r']})
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
    def check_receipt_exists_by_id(receipt_id: int):
        existing_receipt = ReceiptDBService.get_receipt_by_id(receipt_id)
        if not existing_receipt:
            msg = {
                'code': 'RECEIPT_NOT_FOUND',
                'message': f'Receipt with id <{receipt_id}> does not exist.'
            }

            return msg
