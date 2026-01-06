from flask import Blueprint, request
from api.schemas.order_detail import OrderDetailRequestSchema, OrderDetailResponseSchema
from infrastructure.repositories.sale_and_finance_repo.order_detail_repository import OrderDetailRepository
from domain.models.order_detail import OrderDetail
from api.responses import success_response, error_response

order_detail_bp = Blueprint('order_detail_bp', __name__)
repo = OrderDetailRepository()

@order_detail_bp.route('/', methods=['POST'])
def add_order_detail():
    '''
    Add product detail to an order
    ---
    tags:
      - Order Details
    parameters:
      - in: body
        name: body
        schema:
          $ref: '#/components/schemas/OrderDetailRequest'
    responses:
      201:
        description: Detail added successfully
    '''
    try:
        data = request.json
        new_detail = OrderDetail(
            order_id=data['order_id'],
            product_id=data['product_id'],
            unit_id=data['unit_id'],
            order_quantity=data['order_quantity'],
            unit_price=data['unit_price'],
            line_total=data.get('line_total')
        )
        result = repo.add(new_detail)
        return success_response(OrderDetailResponseSchema().dump(result), 201)
    except Exception as e:
        return error_response(str(e), 500)
def add_order_with_details(self, order_model):
        try:
            self.session.add(order_model)
            
            # LOGIC QUAN TRỌNG: Duyệt qua từng món hàng để trừ tồn kho
            for detail in order_model.details:
                product = self.session.query(ProductModel).filter_by(product_id=detail.product_id).first()
                if product:
                    if product.stock_quantity < detail.order_quantity:
                        raise ValueError(f"Sản phẩm {product.product_name} không đủ hàng!")
                    product.stock_quantity -= detail.order_quantity # Trừ kho

            self.session.commit()
            self.session.refresh(order_model)
            return order_model
        except Exception as e:
            self.session.rollback()
            raise e