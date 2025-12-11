from sqlalchemy.orm import Session
from dependency_injector.wiring import inject, Provide
from app.container import Container
from app.model import Customer, Product,  Stock


@inject
def create_customer(session: Session = Provide[Container.session]) -> Customer:
    try:
        customer = Customer(name="John Doe", telephone="123-456-7890", location="New York")
        session.add(customer)
        session.commit()
        session.refresh(customer)
    except Exception as e:
        session.rollback()
        
    return customer

@inject
def create_product(session: Session = Provide[Container.session]):
    example_product = [
        # Shampoo Variants
        {"name": "Shampoo Anti-Dandruff 250ml", "description": "Anti-dandruff formula for flaky scalp", "price": 5.99, "stock_quantity": 120},
        {"name": "Shampoo Anti-Dandruff 500ml", "description": "Anti-dandruff formula for flaky scalp", "price": 9.99, "stock_quantity": 80},
        {"name": "Shampoo Moisturizing 250ml", "description": "Deep hydration for dry hair", "price": 6.49, "stock_quantity": 100},
        {"name": "Shampoo Moisturizing 500ml", "description": "Deep hydration for dry hair", "price": 10.99, "stock_quantity": 75},
        
        # Toothpaste Variants
        {"name": "Toothpaste Whitening 75g", "description": "Advanced whitening formula", "price": 2.99, "stock_quantity": 200},
        {"name": "Toothpaste Whitening 150g", "description": "Advanced whitening formula", "price": 4.99, "stock_quantity": 150},
        {"name": "Toothpaste Sensitive 75g", "description": "Gentle formula for sensitive teeth", "price": 3.49, "stock_quantity": 180},
        {"name": "Toothpaste Sensitive 150g", "description": "Gentle formula for sensitive teeth", "price": 5.99, "stock_quantity": 120},
        
        # Laundry Detergent Variants
        {"name": "Laundry Detergent Liquid 1L", "description": "Concentrated liquid for all fabrics", "price": 7.99, "stock_quantity": 90},
        {"name": "Laundry Detergent Liquid 2L", "description": "Concentrated liquid for all fabrics", "price": 13.99, "stock_quantity": 60},
        {"name": "Laundry Detergent Powder 1kg", "description": "Powerful powder detergent", "price": 6.99, "stock_quantity": 100},
        {"name": "Laundry Detergent Powder 2kg", "description": "Powerful powder detergent", "price": 11.99, "stock_quantity": 70},
        
        # Dish Soap Variants
        {"name": "Dish Soap Lemon 500ml", "description": "Antibacterial with lemon scent", "price": 2.99, "stock_quantity": 150},
        {"name": "Dish Soap Lemon 750ml", "description": "Antibacterial with lemon scent", "price": 3.99, "stock_quantity": 120},
        {"name": "Dish Soap Original 500ml", "description": "Classic grease-cutting formula", "price": 2.49, "stock_quantity": 160},
        {"name": "Dish Soap Original 750ml", "description": "Classic grease-cutting formula", "price": 3.49, "stock_quantity": 130},
        
        # Body Lotion Variants
        {"name": "Body Lotion Cocoa Butter 200ml", "description": "Rich moisturizing lotion", "price": 4.99, "stock_quantity": 110},
        {"name": "Body Lotion Cocoa Butter 400ml", "description": "Rich moisturizing lotion", "price": 8.49, "stock_quantity": 85},
        {"name": "Body Lotion Aloe Vera 200ml", "description": "Soothing aloe vera formula", "price": 4.49, "stock_quantity": 120},
        {"name": "Body Lotion Aloe Vera 400ml", "description": "Soothing aloe vera formula", "price": 7.99, "stock_quantity": 90},
        
        # Deodorant Variants
        {"name": "Deodorant Roll-On Fresh 50ml", "description": "48-hour fresh protection", "price": 3.99, "stock_quantity": 140},
        {"name": "Deodorant Roll-On Sport 50ml", "description": "48-hour sport protection", "price": 4.49, "stock_quantity": 130},
        {"name": "Deodorant Spray Fresh 150ml", "description": "Quick-dry spray formula", "price": 5.99, "stock_quantity": 100},
        {"name": "Deodorant Spray Sport 150ml", "description": "Quick-dry sport formula", "price": 6.49, "stock_quantity": 95},
    ]
    try:
        for item in example_product:
            product = Product(name=item["name"], description=item["description"], price=item["price"])
            session.add(product)
            session.commit()
            session.refresh(product)
            stock = Stock(product_id=product.id, quantity=item["stock_quantity"])
            session.add(stock)
            session.commit()
            session.refresh(stock)
    except Exception as e:
        session.rollback()
        
if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    container.init_resources()  
    create_customer()
    create_product()
    container.shutdown_resources()