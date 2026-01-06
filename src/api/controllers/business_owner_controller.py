from flask import Blueprint, request, jsonify
from services.business_owner_service import BusinessOwnerService
from infrastructure.repositories.access_and_identity_repo.business_owner_repository import BusinessOwnerRepository
from infrastructure.databases.mssql import session
from api.middlewares.auth_middleware import token_required
business_owner_bp = Blueprint('business_owner_bp', __name__)

owner_repo = BusinessOwnerRepository(session)
owner_service = BusinessOwnerService(owner_repo)

@business_owner_bp.route('/', methods=['POST'])
@token_required
def register_new_owner():
    """
    Tạo chủ cửa hàng mới
    ---
    tags: [Business Owners]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          required: [owner_name, email, password, phone_number, admin_id, plan_id]
          properties:
            owner_name: {type: string, example: "Nguyen Van A"}
            email: {type: string, example: "a@gmail.com"}
            phone_number: {type: string, example: "0901234567"}
            password: {type: string, example: "123456"}
            admin_id: {type: integer, example: 1}
            plan_id: {type: integer, example: 1}
    responses:
      201: {description: "Thành công"}
    """
    
    try:
        data = request.get_json()
        result = owner_service.create_owner(data)
        return jsonify({"message": "Thành công", "id": result.owner_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@business_owner_bp.route('/', methods=['GET'])
@token_required
def get_all_business_owners():
    """
    Lấy danh sách chủ doanh nghiệp
    ---
    tags: [Business Owners]
    security: [{BearerAuth: []}]
    responses:
      200:
        description: Thành công
    """
    try:
        owners = owner_service.list_all_owners() # Gọi đúng tên hàm trong Service
        return jsonify([
            {
                "id": o.owner_id, 
                "name": o.owner_name, 
                "email": o.email,
                "status": o.account_status
            } for o in owners
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500