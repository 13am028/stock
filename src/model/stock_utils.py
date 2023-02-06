from typing import Any, List

from model.model import Products, Stock, session, session_commit

product_not_found = "Product Not Found !"


def find_product(lid: str, pid: str) -> Stock:
    """Find the product with given location id and product id."""
    return (
        Stock.query.filter(Stock.location_id == lid)
        .filter(Stock.product_id == pid)
        .first()
    )


def product_to_stock(lid: str, pid: str, stock_num: str) -> str:
    """Add product to stock. If it already exists, change the number of stock."""
    new_stock: Stock = Stock(location_id=lid, product_id=pid, stock=stock_num)
    if int(stock_num) < 0:
        return "Stock Cannot Be Negative !"
    products_in_stock: List[Stock] = Stock.query.filter(Stock.location_id == lid).all()
    for product in products_in_stock:
        if pid == str(product.product_id):
            product.stock = stock_num
            return session_commit()
    session.add(new_stock)
    return session_commit()


def increase_stock(lid: str, pid: str) -> str:
    """Increase stock of a product in location."""
    product: Products = find_product(lid, pid)
    if product is None:
        return product_not_found
    product.stock += 1
    return session_commit()


def decrease_stock(lid: str, pid: str) -> str:
    """Decrease stock of a product in location."""
    product: Products = find_product(lid, pid)
    if product is None:
        return product_not_found
    if product.stock > 0:
        product.stock -= 1
    return session_commit()


def delete_stock(lid: str, pid: str) -> str:
    """Delete product from location stock."""
    product: Products = find_product(lid, pid)
    if product is None:
        return product_not_found
    session.delete(product)
    return session_commit()


def get_products(lid: str) -> List[Any]:
    """Get all products given location id."""
    ret: List[Any] = (
        session.query(Stock, Products)
        .join(Products)
        .filter(Stock.location_id == lid)
        .all()
    )
    ret.sort(key=lambda x: x[1].product_name)
    return ret
