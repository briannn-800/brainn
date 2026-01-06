from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from services.sale_and_finance_service.payment_service import PaymentService
from infrastructure.repositories.sale_and_finance_repo.payment_repository import PaymentRepository
from infrastructure.databases.mssql import session
from infrastructure.repositories.sale_and_finance_repo.debt_repository import DebtRepository
payment_bp = Blueprint('payment_bp', __name__)
repo = PaymentRepository(session)
debt_repo = DebtRepository(session)
service = PaymentService(repo, debt_repo)

@payment_bp.route('/', methods=['POST'])
@token_required
def process_debt_payment():
    """
    Thanh toán công nợ
    ---
    tags: [Finance & Debt]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            debt_id: {type: integer, example: 1}
            amount: {type: number, example: 200000}
            payment_method: {type: string, example: "Transfer"}
    responses:
      201: {description: "Thành công"}
    """
    