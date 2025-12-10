from sqlalchemy.orm import Session
from dependency_injector.wiring import inject, Provide
from app.container import Container
from app.model import Customer, Product, Order, Stock


@inject
def create_customer(session: Session = Provide[Container.session]) -> Customer:
    customer = Customer(name="John Doe", telephone="123-456-7890", location="New York")
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@inject
def create_product(session: Session = Provide[Container.session]) -> Product:
    example_product = [
        {"name": "Laptop", "description": "A high-performance laptop", "price": 1200.00, "stock_quantity": 10},
        {"name": "Smartphone", "description": "A latest model smartphone", "price": 800.00, "stock_quantity": 25},
        {"name": "Headphones", "description": "Noise-cancelling headphones", "price": 150.00, "stock_quantity": 50},
        {"name": "Monitor", "description": "4K UHD Monitor", "price": 400.00, "stock_quantity": 15},
        {"name": "Keyboard", "description": "Mechanical keyboard", "price": 100.00, "stock_quantity": 30},
    ]
    for item in example_product:
        product = Product(name=item["name"], description=item["description"], price=item["price"])
        session.add(product)
        session.commit()
        session.refresh(product)
        stock = Stock(product_id=product.id, quantity=item["stock_quantity"])
        session.add(stock)
        session.commit()
        session.refresh(stock)

if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    container.init_resources()  
    # create_customer()
    create_product()
    container.shutdown_resources()