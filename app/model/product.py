from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db import Base

if TYPE_CHECKING:
    from model.stock import Stock
    from model.order import Order
    
class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column("id",Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column("name", String,  nullable=False)
    description: Mapped[str] = mapped_column("description", String,  nullable=False)
    price: Mapped[float] = mapped_column("price", Float,  nullable=False)
    stock: Mapped["Stock"] = relationship("Stock", back_populates="product", uselist=False, cascade="all, delete-orphan")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="product", cascade="all, delete-orphan")