from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text, DateTime


Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    seller = Column(String, nullable=False)


class DealStatus:
    NEW = "New"
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    COMPLETED = "Completed"


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    buyer = Column(String, nullable=False)
    seller = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(String, default=DealStatus.NEW, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    payment_link = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<Deal(id={self.id}, buyer={self.buyer}, seller={self.seller}, "
            f"product_name={self.product_name}, status={self.status})>"
        )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
