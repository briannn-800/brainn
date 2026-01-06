from flask import Blueprint, request, jsonify
from infrastructure.repositories.sale_and_finance_repo.customer_repository import CustomerRepository
from services.customer_service import CustomerService
from infrastructure.databases.mssql import session
from api.middlewares.auth_middleware import token_required

customer_bp = Blueprint('customer_bp', __name__)

cust_repo = CustomerRepository(session)
cust_service = CustomerService(cust_repo)

@customer_bp.route('/', methods=['POST'])
@token_required
def add_new_customer(): # Tên hàm duy nhất
    """
    Thêm khách hàng
    ---
    tags: [Customers]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          required: [customer_name, owner_id]
          properties:
            customer_name: {type: string, example: "Nguyen Van B"}
            phone_number: {type: string, example: "0901234567"}
            address: {type: string, example: "123 Le Loi, TP.HCM"}
            owner_id: {type: integer, example: 1}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        result = cust_service.create_customer(data)
        return jsonify({"message": "Thành công", "id": result.customer_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@customer_bp.route('/', methods=['GET'])
@token_required
def get_all_customers():
    """
    Lấy danh sách khách hàng
    ---
    tags: [Customers]
    security: [{BearerAuth: []}]
    responses:
      200:
        description: Thành công
    """
    try:
        customers = cust_service.list_customers()
        return jsonify([
            {
                "id": c.customer_id, 
                "name": c.customer_name, 
                "phone": c.phone_number,
                "address": c.address,
                "debt": float(c.total_outstanding_debt)
            } for c in customers
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500