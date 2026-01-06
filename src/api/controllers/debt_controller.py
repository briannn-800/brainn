from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from services.debt_service import DebtService
from infrastructure.repositories.debt_repository import DebtRepository
from infrastructure.databases.mssql import session

debt_bp = Blueprint('debt_bp', __name__)
repo = DebtRepository(session)
service = DebtService(repo)

@debt_bp.route('/', methods=['POST'])
@token_required
def create_customer_debt():
    """
    Ghi nhận công nợ mới
    ---
    tags: [Finance & Debt]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            order_id: {type: integer, example: 1}
            customer_id: {type: integer, example: 1}
            debt_amount: {type: number, example: 500000}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        result = service.create_debt_from_order(data['order_id'], data['customer_id'], data['debt_amount'])
        return jsonify({"id": result.debt_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400