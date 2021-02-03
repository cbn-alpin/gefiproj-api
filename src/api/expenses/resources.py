from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from src.api.users.auth_resources import admin_required

from src.api.expenses.db_services import ExpenseDBService
from src.api.expenses.entities import ExpenseSchema, Expense
from src.api.expenses.validation_service import ExpenseValidationService

resources = Blueprint('expenses', __name__)

@resources.route('/api/expenses', methods=['GET'])
@jwt_required
def get_expenses():
    try:
        current_app.logger.debug('In GET /api/expenses')
        response = ExpenseDBService.get_all_expenses()
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/expenses', methods=['POST'])
@jwt_required
def add_expense():
    try:
        current_app.logger.debug('In POST /api/expenses')
        posted_expense_data = request.get_json()

        # validate expense
        validation_errors = ExpenseValidationService.validate_post(posted_expense_data)
        if len(validation_errors) > 0:
            return jsonify({
                'message': 'A validation error occured',
                'errors': validation_errors
            }), 422
        # check
        ExpenseDBService.check_unique_year(posted_expense_data['annee_d'])
        
        created_expense = ExpenseDBService.insert(posted_expense_data)
        return jsonify(created_expense), 201
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
    except Exception as error:
        return jsonify(error.args[0]), error.args[1]


@resources.route('/api/expenses/<int:expense_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_expense(expense_id):
    try:
        current_app.logger.debug('In PUT /api/expenses/<int:expense_id>')
        # Load data
        data = request.get_json()
        if 'id_d' not in data:
            data['id_d'] = expense_id
            
        # validate fields to update
        validation_errors = ExpenseValidationService.validate_post(data)
        if len(validation_errors) > 0:
            return jsonify({
                'message': 'A validation error occured',
                'errors': validation_errors
            }), 422
        # check
        ExpenseDBService.check_exist_expense(expense_id)
        ExpenseDBService.check_unique_year(data['annee_d'], expense_id)
        
        response = ExpenseDBService.update(data)
        return jsonify(response), 200
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
    except Exception as error:
        return jsonify(error.args[0]), error.args[1]
    
    
@resources.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_expense(expense_id):
    try:
        current_app.logger.debug('In DELETE /api/expenses/<int:expense_id>')
        # check
        ExpenseDBService.check_exist_expense(expense_id)

        response = ExpenseDBService.delete(expense_id)
        return jsonify(response), 204
    except ValueError as error:
        return jsonify(error.args[0]), error.args[1]
