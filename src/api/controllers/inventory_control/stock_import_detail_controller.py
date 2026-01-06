from flask import Blueprint, request, jsonify
from api.middlewares.auth_middleware import token_required
from infrastructure.repositories.inventory_repo.stock_import_detail_repository import StockImportDetailRepository
from services.inventory_service.stock_import_detail_stock import StockImportDetailService

stock_import_detail_bp = Blueprint('stock_import_detail_bp', __name__)
repo = StockImportDetailRepository()
service = StockImportDetailService(repo)

@stock_import_detail_bp.route('/', methods=['POST'])
@token_required
def add_detail():
    data = request.get_json()
    try:
        detail = service.create_detail(data)
        return jsonify({
            "message": "Thêm chi tiết nhập hàng thành công", 
            "detail_id": detail.detail_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@stock_import_detail_bp.route('/import/<int:import_id>', methods=['GET'])
@token_required
def get_details(import_id):
    details = service.get_details_by_import(import_id)
    result = []
    for d in details:
        result.append({
            "detail_id": d.detail_id,
            "product_id": d.product_id,
            "quantity": d.quantity,
            "unit_price": float(d.unit_price)
        })
    return jsonify(result), 200