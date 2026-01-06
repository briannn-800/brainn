from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base
import datetime

class SupplierModel(Base):
    __tablename__ = 'suppliers'
    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'))
    supplier_name = Column(String(100), nullable=False) # Dùng String cho MSSQL
    phone_number = Column(String(20))
    tax_code = Column(String(50))

class StockImportModel(Base):
    __tablename__ = 'stock_imports'
    import_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'))
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'))
    import_date = Column(DateTime, default=datetime.datetime.utcnow)
    total_amount = Column(Numeric(18, 2), default=0) # Chuẩn cho báo cáo kế toán

class StockImportDetailModel(Base):
    __tablename__ = 'stock_import_details'
    detail_id = Column(Integer, primary_key=True, autoincrement=True)
    import_id = Column(Integer, ForeignKey('stock_imports.import_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(18, 2), nullable=False)