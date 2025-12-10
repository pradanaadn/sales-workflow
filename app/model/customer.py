from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db import Base

if TYPE_CHECKING:
    from model.order import Order

class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column("id",Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column("name", String,  nullable=False)
    telephone: Mapped[str] = mapped_column("telephone", String, unique=True, nullable=False)
    location: Mapped[str] = mapped_column("location", String,  nullable=False)
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="customer", cascade="all, delete-orphan")