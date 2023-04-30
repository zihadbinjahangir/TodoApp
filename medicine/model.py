from sqlalchemy import Integer, Float, String, Column
from database import Base

class Medicine(Base):
    __tablename__ = 'medicine_info'

    id = Column(Integer, primary_key=True)
    product_name = Column(String(255))
    generic_name = Column(String(255))
    dosage_form = Column(String(255))
    strength = Column(String(255))
    manufacturer = Column(String(255))
    price_type = Column(String(255))
    price = Column(Float)
