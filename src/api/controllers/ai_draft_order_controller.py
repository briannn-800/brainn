from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from services.ai_draft_order_service import AIDraftOrderService
from infrastructure.repositories.ai_draft_order_repository import AIDraftOrderRepository
from infrastructure.databases.mssql import session


ai_draft_order_bp = Blueprint('ai_draft_order_bp', __name__)
repo = AIDraftOrderRepository(session)
service = AIDraftOrderService(repo)

@ai_draft_order_bp.route('/', methods=['POST'])
@token_required
def create_ai_draft():
    """
    AI tạo đơn hàng nháp từ giọng nói
    ---
    tags: [AI Features]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          properties:
            employee_id: {type: integer, example: 1}
            customer_id: {type: integer, example: 1}
            voice_content: {type: string, example: "Bán cho anh 2 thùng bia Sài Gòn"}
    responses:
      201: {description: "Đã tạo bản nháp"}
    """
    try:
        data = request.get_json()
        result = service.create_draft_from_voice(data)
        return jsonify({"draft_id": result.draft_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400