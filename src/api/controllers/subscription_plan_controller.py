from flask import Blueprint, request, jsonify
from infrastructure.repositories.access_and_identity_repo.subscription_plan_repository import SubscriptionPlanRepository
from services.subscription_plan_service import SubscriptionPlanService
from infrastructure.databases.mssql import session
from api.middlewares.auth_middleware import token_required

subscription_plan_bp = Blueprint('subscription_plan_bp', __name__)

plan_repo = SubscriptionPlanRepository(session)
plan_service = SubscriptionPlanService(plan_repo)

@subscription_plan_bp.route('/', methods=['POST'])
@token_required
def create_new_subscription_plan(): # Tên hàm duy nhất
    """
    Tạo gói cước dịch vụ mới
    ---
    tags: [Subscriptions]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          required: [plan_name, duration, price]
          properties:
            plan_name: {type: string, example: "Gói Premium 12 tháng"}
            duration: {type: integer, example: 12}
            price: {type: number, example: 1200000}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        result = plan_service.create_plan(data)
        return jsonify({"message": "Tạo gói cước thành công", "id": result.plan_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@subscription_plan_bp.route('/', methods=['GET'])
@token_required
def list_all_plans(): # Tên hàm duy nhất
    """
    Lấy danh sách các gói cước
    ---
    tags: [Subscriptions]
    security: [{BearerAuth: []}]
    responses:
      200:
        description: Thành công
    """
    try:
        plans = plan_service.list_plans()
        return jsonify([
            {
                "id": p.plan_id, 
                "name": p.plan_name, 
                "duration": p.duration,
                "price": float(p.price)
            } for p in plans
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500