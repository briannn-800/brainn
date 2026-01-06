from datetime import datetime
from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel

class OrderService:
    def __init__(self, repository):
        self.repository = repository

    def create_order(self, data, employee_id):
        # 1. Khởi tạo Header hóa đơn
        new_order = OrderModel(
            customer_id=data.get('customer_id'),
            employee_id=employee_id, # Lấy từ token
            order_date=datetime.now(),
            order_status="Completed",
            payment_method=data.get('payment_method', 'Cash'),
            total_amount=0
        )

        details = []
        final_total = 0

        # 2. Xử lý danh sách OrderDetail
        if 'items' in data:
            for item in data['items']:
                line_total = int(item['quantity']) * float(item['unit_price'])
                detail = OrderDetailModel(
                    product_id=item['product_id'],
                    unit_id=item['unit_id'],
                    order_quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    line_total=line_total
                )
                details.append(detail)
                final_total += line_total

        new_order.details = details
        new_order.total_amount = final_total
        return self.repository.add_order_with_details(new_order)