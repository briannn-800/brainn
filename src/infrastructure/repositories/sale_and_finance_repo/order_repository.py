from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.inventory.product_model import ProductModel
from infrastructure.databases.mssql import session

class OrderRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add_order_with_details(self, order_model):
        try:
            self.session.add(order_model)
            
            # LOGIC CẨN THẬN: Duyệt qua từng món hàng để trừ tồn kho
            for detail in order_model.details:
                product = self.session.query(ProductModel).filter_by(product_id=detail.product_id).first()
                if product:
                    if product.stock_quantity < detail.order_quantity:
                        raise ValueError(f"Sản phẩm {product.product_name} không đủ hàng trong kho!")
                    product.stock_quantity -= detail.order_quantity # Trừ tồn kho
            
            self.session.commit()
            self.session.refresh(order_model)
            return order_model
        except Exception as e:
            self.session.rollback()
            raise e