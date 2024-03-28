from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship


# User management yet to be added.
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    created_by_ip = Column(String)
    is_active = Column(Boolean, default=True)
    is_disabled = Column(Boolean, default=False)
