from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required

from src.api.expenses.db_services import ExpenseDBService
from src.api.expenses.entities import ExpenseSchema, Expense
from src.api.expenses.validation_service import ExpenseValidationService
from src.api.users.auth_resources import admin_required

resources = Blueprint('expenses', __name__)


@resources.route('/api/expenses', methods=['POST'])
@jwt_required
@admin_required
def add_expense():
    current_app.logger.debug('In POST /api/expenses')
    posted_expense_data = request.get_json()

    # validate expense
    validation_errors = ExpenseValidationService.validate_post(posted_expense_data)
    if len(validation_errors) > 0:
        return jsonify({
            'message': 'A validation error occured',
            'errors': validation_errors
        }), 422

    # save expense
    posted_expense = ExpenseSchema(only=('annee_d', 'montant_d')).load(posted_expense_data)
    expense = Expense(**posted_expense)

    created_expense = ExpenseDBService.insert(expense)
    return jsonify(created_expense), 201
