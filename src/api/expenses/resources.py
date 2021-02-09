from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from src.api.users.auth_resources import admin_required

from src.api.expenses.db_services import ExpenseDBService
from src.api.expenses.validation_service import ExpenseValidationService

resources = Blueprint('expenses', __name__)


@resources.route('/api/expenses', methods=['GET'])
@jwt_required
def get_expenses():
    """This function get all expenses

    Returns:
        Response: list of expenses
    """
    current_app.logger.debug('In GET /api/expenses')
    response = None
    try:
        response = ExpenseDBService.get_all_expenses()
        response = jsonify(response), 200
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    finally:
        return response


@resources.route('/api/expenses', methods=['POST'])
@jwt_required
def add_expense():
    """This function created a new funder

    Returns:
        Response: expense created
    """
    current_app.logger.debug('In POST /api/expenses')
    response = None
    try:
        posted_expense = request.get_json()
        # Validate expense
        ExpenseValidationService.validate(posted_expense)
        # Check year is unique
        ExpenseDBService.check_unique_year(posted_expense['annee_d'])
        
        created_expense = ExpenseDBService.insert(posted_expense)
        response = jsonify(created_expense), 201
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    finally:
        return response


@resources.route('/api/expenses/<int:expense_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_expense(expense_id: int):
    """This function update a data of expense

    Args:
        expense_id (int): id of expense

    Returns:
        Response: description of expense
    """
    current_app.logger.debug('In PUT /api/expenses/<int:expense_id>')
    response = None
    try:
        # Load data
        data = request.get_json()
        if 'id_d' not in data:
            data['id_d'] = expense_id
            
        # Validate fields to update
        ExpenseValidationService.validate(data)
        # Check expense exist
        ExpenseDBService.get_expense_by_id(expense_id)
        # Check year expense is unique
        ExpenseDBService.check_unique_year(data['annee_d'], expense_id)
        
        response = ExpenseDBService.update(data)
        response = jsonify(response), 200
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    finally:
        return response


@resources.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_expense(expense_id: int):
    """This function delete an expense

    Args:
        expense_id (int): id of expense
    Returns:
    """
    current_app.logger.debug('In DELETE /api/expenses/<int:expense_id>')
    response = None
    try:
        # Check if expense exists
        expense = ExpenseDBService.get_expense_by_id(expense_id)

        response = ExpenseDBService.delete(expense_id, expense['annee_d'])
        response = jsonify(response), 204
    except (ValueError, Exception) as error:
        current_app.logger.error(error)
        response = jsonify(error.args[0]), error.args[1]
    finally:
        return response
