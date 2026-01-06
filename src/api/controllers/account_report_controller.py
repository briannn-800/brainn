from flask import Blueprint, jsonify
from api.middlewares.auth_middleware import token_required
# Thay vì import từ finance_service chung chung
from services.account_report_service import AccountReportService
from infrastructure.repositories.sale_and_finance_repo.account_report_repository import AccountReportRepository
account_report_bp = Blueprint('account_report_bp', __name__)

@account_report_bp.route('/', methods=['POST'])
@token_required
def create_report():
    """
    Tạo báo cáo doanh thu
    ---
    tags: [Reports]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            owner_id: {type: integer, example: 1}
            report_type: {type: string, example: "Monthly"}
            report_name: {type: string, example: "Báo cáo tháng 1"}
    responses:
      201: {description: "Thành công"}
    """
