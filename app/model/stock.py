from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db import Base

if TYPE_CHECKING:
    from model.product import Product
    
class Stock(Base):
    
    __tablename__ = "stock"
    id: Mapped[int] = mapped_column("id",Integer, autoincrement=True, primary_key=True)
    product_id: Mapped[int] = mapped_column("product_id", Integer, ForeignKey("product.id"), unique=True, nullable=False)
    quantity: Mapped[int] = mapped_column("quantity", Integer, nullable=False)
    product: Mapped["Product"] = relationship("Product", back_populates="stock")