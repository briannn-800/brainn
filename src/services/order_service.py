from datetime import datetime
from infrastructure.models.order_model import OrderModel
from infrastructure.models.order_detail_model import OrderDetailModel

class OrderService:
    def __init__(self, repository):
        self.repository = repository

    def create_order(self, data):
        # 1. Tạo thông tin chung (Header)
        new_order = OrderModel(
            customer_id=data['customer_id'],
            employee_id=data['employee_id'],
            order_date=datetime.now(),
            order_status="Completed", # Giả sử bán tại quầy là xong luôn
            payment_method=data.get('payment_method', 'Cash'),
            total_amount=0 # Sẽ tính lại ở dưới
        )

        details = []
        final_total = 0

        # 2. Xử lý từng món hàng (Items)
        if 'items' in data:
            for item in data['items']:
                quantity = int(item['quantity'])
                price = float(item['unit_price'])
                line_total = quantity * price
                
                detail = OrderDetailModel(
                    product_id=item['product_id'],
                    unit_id=item['unit_id'],
                    order_quantity=quantity,
                    unit_price=price,
                    line_total=line_total
                )
                details.append(detail)
                final_total += line_total

        # 3. Gán danh sách chi tiết và tổng tiền vào đơn hàng
        new_order.details = details
        new_order.total_amount = final_total

        return self.repository.add_order_with_details(new_order)