from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from infrastructure.repositories.inventory_repo.stock_import_detail_repository import StockImportDetailRepository
from services.inventory_service.stock_import_detail_stock import StockImportDetailService

stock_import_detail_bp = Blueprint('stock_import_detail_bp', __name__)
repo = StockImportDetailRepository()
service = StockImportDetailService(repo)


@stock_import_detail_bp.route('/import/<int:import_id>', methods=['GET'])
@token_required
def get_details(import_id):
    """
    Lấy chi tiết của một phiếu nhập hàng
    ---
    tags: [Inventory Control]
    security: [{BearerAuth: []}]
    parameters:
      - name: import_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: "Danh sách chi tiết sản phẩm"}
    """
    # ... logic xử lý ...
    data = request.get_json()
    try:
        detail = service.create_detail(data)
        return jsonify({
            "message": "Thêm chi tiết nhập hàng thành công", 
            "detail_id": detail.detail_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

