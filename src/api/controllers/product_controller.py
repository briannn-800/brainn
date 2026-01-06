from flask import Blueprint, request, jsonify
from services.product_service import ProductService
from infrastructure.repositories.inventory_repo.product_repository import ProductRepository
from infrastructure.databases.mssql import session
from api.middlewares.auth_middleware import token_required

product_bp = Blueprint('product_bp', __name__)

product_repo = ProductRepository(session)
product_service = ProductService(product_repo)

@product_bp.route('/', methods=['POST'])
@token_required
def create_new_product():
    """
    Thêm sản phẩm mới (Tự động gán Owner ID từ Token)
    ---
    tags: [Inventory]
    security: [{BearerAuth: []}]
    parameters:
      - in: body
        name: body
        schema:
          required: [product_name, selling_price]
          properties:
            product_name: {type: string, example: "Bia Sài Gòn Lager"}
            selling_price: {type: number, example: 18000}
            stock_quantity: {type: integer, example: 50}
    responses:
      201: {description: "Tạo sản phẩm thành công"}
      401: {description: "Token không hợp lệ"}
    """
    try:
        data = request.get_json()
        
      
        data['owner_id'] = request.current_user_id 
        
        product = product_service.create_product(data)
        
        return jsonify({
            "message": "Tạo sản phẩm thành công",
            "product_id": product.product_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@product_bp.route('/', methods=['GET'])
@token_required
def list_products_by_owner():
    """
    Lấy danh sách sản phẩm (Chỉ lấy đúng của shop đang đăng nhập)
    ---
    tags: [Inventory]
    security: [{BearerAuth: []}]
    responses:
      200:
        description: Danh sách sản phẩm thành công
    """
    try:
        # Lấy ID từ Token để làm điều kiện lọc
        owner_id = request.current_user_id 
        
        # Gọi Service để tìm sản phẩm có owner_id khớp với ID này
        products = product_service.get_products_by_owner(owner_id) 

        result = []
        for p in products:
            result.append({
                "product_id": p.product_id,
                "product_name": p.product_name,
                "selling_price": float(p.selling_price) if p.selling_price else 0,
                "stock_quantity": p.stock_quantity
            })
        return jsonify({"data": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500