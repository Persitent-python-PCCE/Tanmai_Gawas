from models.product import Product

class ProductService:
    def __init__(self, product_dao):
        self.product_dao = product_dao

    def create_product(self, data):
        if not data:
            raise ValueError("product data cannot be null")

        id = data.get("id")
        name = data.get("name")
        category = data.get("category")
        price = data.get("price")
        quantity = data.get("quantity")
        description = data.get("description")

        if not name:
            raise ValueError("Name is required")

        if not category:
            raise ValueError("Email is required")

        if price is None:
            raise ValueError("Age is required")

        if quantity is None:
            raise ValueError("Quantity is required")

        if description is None:
            raise ValueError("description is required")

        product = Product(
            id=id,
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            description=description
        )

        return self.product_dao.create_product(product)

    def get_all_products(self):
        products = self.product_dao.get_all_products()
        if products is None:
            raise ValueError("No products found")
        return products

    def get_product_by_id(self, p_id):
        product = self.product_dao.get_product_by_id(p_id)
        if product is None:
            raise ValueError(f"Product with id {p_id} not found")
        return product

    def update_product(self, p_id, data):
        product = self.product_dao.update_product(p_id, data.get("name"), data.get("category"), data.get("price"), data.get("quantity"), data.get("description"))
        if product is None:
            raise ValueError(f"Product with id {p_id} not found")
        return product

    def delete_product(self, p_id):
        product = self.product_dao.delete_product(p_id)
        if product is None:
            raise ValueError(f"Product with id {p_id} not found")
        return p_id