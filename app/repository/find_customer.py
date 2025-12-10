from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.model import Customer


def find_customer_by_telephone(session: Session, telephone: str) -> Customer | None:
    customer = session.query(Customer).filter(
        and_(Customer.telephone == telephone)
    ).first()
    return customer


def create_customer(session: Session, name: str, location: str, telephone: str) -> Customer:
    new_customer = Customer(
        name=name,
        location=location,
        telephone=telephone
    )
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    return new_customer