
from models.product import Product
from config.database import db

class ProductDAO():
    def create_product(self, product):
        try:
            db.session.add(product)
            db.session.commit()
            return product
        except Exception as e:
            db.session.rollback()
            print("Error creating product:", e)

    def get_all_products(self):
        products = Product.query.all()
        return products

    def get_product_by_id(self, p_id):
        product = Product.query.get(p_id)
        return product

    def update_product(self, p_id, name, category, price, quantity, description):
        product = db.session.get(Product, p_id)
        if product is None:
            return None
        if name:
            product.name = name
        if category:
            product.category = category
        if price:
            product.price = price
        if quantity:
            product.quantity = quantity
        if description:
            product.description = description
        db.session.commit()
        return product

    def delete_product(self, p_id):
        product = db.session.get(Product, p_id)
        if product is None:
            return None
        db.session.delete(product)
        db.session.commit()
        return product
