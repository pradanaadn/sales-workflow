from sqlalchemy import and_

from app.model import Product, Stock


def check_stock(session, product_name:str) -> list[Stock] | list:
    stock = session.query(Stock).join(Product).filter(
        and_(Product.name.like(f"%{product_name}%"), Stock.quantity > 0)
    ).all()
    return stock if stock else []


# if __name__ == "__main__":
#     from app.container import Container
#     from sqlalchemy.orm import Session

#     container = Container()
#     container.wire(modules=[__name__])
#     session: Session = container.session()

#     result = check_stock(session, "phone")
#     for stock in result:
#         print(f"Product ID: {stock.product_id}, Name: {stock.product.name}, Quantity: {stock.quantity}")

#     container.shutdown_resources()