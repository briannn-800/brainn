from infrastructure.models.customer_model import CustomerModel
from infrastructure.databases.mssql import session

class CustomerRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, name, phone, address, owner_id):
        # Thêm owner_id vào đây để khớp với Model
        db_cust = CustomerModel(
            customer_name=name, 
            phone_number=phone, 
            address=address,
            owner_id=owner_id
        )
        try:
            self.session.add(db_cust)
            self.session.commit()
            self.session.refresh(db_cust)
            return db_cust
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all(self):
        return self.session.query(CustomerModel).all()