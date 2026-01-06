from flask import Blueprint, request, jsonify
from services.unit_service import UnitService
from infrastructure.repositories.unit_repository import UnitRepository
from infrastructure.databases.mssql import session
from api.middlewares.auth_middleware import token_required

unit_bp = Blueprint('unit_bp', __name__)

unit_repo = UnitRepository(session)
unit_service = UnitService(unit_repo)

@unit_bp.route('/', methods=['POST'])
@token_required
def create_new_unit(): # Tên hàm duy nhất
    """
    Tạo đơn vị tính (Thùng, Lon, Cái)
    ---
    tags: [Inventory]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          required: [unit_name, product_id]
          properties:
            unit_name: {type: string, example: "Thùng"}
            product_id: {type: integer, example: 1}
            conversion_rate: {type: number, example: 24}
            is_base_unit: {type: boolean, example: false}
    responses:
      201: {description: "Thành công"}
    """
    try:
        data = request.get_json()
        # BỔ SUNG LOGIC GỌI SERVICE (Nãy bạn đang để trống chỗ này)
        result = unit_service.create_unit(data)
        return jsonify({"message": "Thành công", "id": result.unit_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@unit_bp.route('/product/<int:product_id>', methods=['GET'])
@token_required
def list_units_by_product(product_id): # Tên hàm duy nhất
    """
    Lấy đơn vị tính theo sản phẩm
    ---
    tags: [Inventory]
    security: [{BearerAuth: []}]
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Thành công
    """
    try:
        units = unit_service.get_units_by_product(product_id)
        return jsonify([
            {
                "id": u.unit_id, 
                "name": u.unit_name, 
                "rate": float(u.conversion_rate) if u.conversion_rate else 1,
                "is_base": u.is_base_unit
            } for u in units
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500