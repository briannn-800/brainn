from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel
from infrastructure.databases.mssql import session

class OrderRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add_order_with_details(self, order_model):
        try:
            self.session.add(order_model)
            # Khi commit, SQLAlchemy sẽ tự động lưu luôn cả list 'details' bên trong order_model
            self.session.commit()
            self.session.refresh(order_model)
            return order_model
        except Exception as e:
            self.session.rollback() # Hủy nếu có lỗi để tránh sai lệch tiền
            raise e
    def get_all(self):
        return self.session.query(OrderModel).all()