class CustomerService:
    def __init__(self, repository):
        self.repository = repository

    def create_customer(self, data):
        if not data.get('customer_name'):
            raise ValueError("Tên khách hàng không được để trống")
        
        # Truyền thêm owner_id từ data xuống Repository
        return self.repository.add(
            name=data['customer_name'], 
            phone=data.get('phone_number'), 
            address=data.get('address'),
            owner_id=data.get('owner_id')
        )

    def list_customers(self):
        return self.repository.get_all()