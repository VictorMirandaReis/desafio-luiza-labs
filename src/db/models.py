from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, unique=True, index=True)
    name = Column(String(45), nullable=False)

    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    external_order_id = Column(Integer, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    purchase_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="orders")
    products = relationship("OrderProduct", back_populates="order")


class OrderProduct(Base):
    __tablename__ = "order_products"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    external_product_id = Column(Integer, index=True)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="products")
