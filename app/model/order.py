from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db import Base

if TYPE_CHECKING:
    from model.customer import Customer
    from model.product import Product

class Order(Base):
    __tablename__ = "order"
    
    id: Mapped[int] = mapped_column("id",Integer, autoincrement=True, primary_key=True)
    customer_id: Mapped[int] = mapped_column("customer_id", Integer, ForeignKey("customer.id"), nullable=False)
    product_id: Mapped[int] = mapped_column("product_id", Integer, ForeignKey("product.id"), nullable=False)
    quantity: Mapped[int] = mapped_column("quantity", Integer, nullable=False)
    total_price: Mapped[float] = mapped_column("total_price", Float, nullable=False)
    customer: Mapped["Customer"] = relationship("Customer", back_populates="orders")
    product: Mapped["Product"] = relationship("Product", back_populates="orders")