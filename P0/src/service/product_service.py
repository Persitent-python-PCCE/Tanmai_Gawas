from src.models.product import Product
from src.utils.logger import log_action
from src.utils.query import QuerySpec, PageResult
from src.dao.product_dao import ALLOWED_SORT_FIELDS

class ProductService:
    def __init__(self, product_dao):
        self.product_dao = product_dao

    def get_all_products(self):
        rows = self.product_dao.get_all()
        return [
            Product(r["id"], r["name"], r["description"], r["price"], r["stock"])
            for r in rows
        ]

    def get_product_by_id(self, product_id):
        return self.product_dao.get_by_id(product_id)

    def add_product(self, name, description, price, stock, admin_full_name):
        name = name.strip()
        if not name:
            raise ValueError("Product name cannot be empty.")
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")

        existing = self.product_dao.get_by_name(name)
        if existing:
            raise ValueError(f"Product '{name}' already exists.")

        product_id = self.product_dao.create(name, description, price, stock)
        log_action(
            f"Admin '{admin_full_name}' added product: ID={product_id}, "
            f"Name='{name}', Stock={stock}"
        )
        return product_id

    def update_product(self, product_id, name=None, description=None, price=None, stock=None, admin_full_name=None):
        prod = self.get_product_by_id(product_id)
        if not prod:
            raise ValueError("Product not found.")

        fields = {}
        if name is not None:
            name = name.strip()
            if not name:
                raise ValueError("Product name cannot be empty.")
            fields["name"] = name
        if description is not None:
            fields["description"] = description
        if price is not None:
            if price <= 0:
                raise ValueError("Price must be greater than zero.")
            fields["price"] = price
        if stock is not None:
            if stock < 0:
                raise ValueError("Stock cannot be negative.")
            fields["stock"] = stock

        if not fields:
            return False

        updated = self.product_dao.update(product_id, fields)
        if updated:
            log_action(
                f"Admin '{admin_full_name}' updated product ID {product_id}. "
                f"Updated fields: {', '.join(fields.keys())}"
            )
        return updated

    def delete_product(self, product_id, admin_full_name):
        prod = self.get_product_by_id(product_id)
        if not prod:
            raise ValueError("Product not found.")

        deleted = self.product_dao.delete(product_id)
        if deleted:
            log_action(f"Admin '{admin_full_name}' deleted product ID {product_id} ('{prod.name}')")
        return deleted

    def browse(self, filters=None, search=None, sort_by=None, sort_dir="ASC", page=1, page_size=10):
        if sort_by and sort_by not in ALLOWED_SORT_FIELDS:
            raise ValueError(f"Cannot sort by '{sort_by}'. Allowed: {', '.join(ALLOWED_SORT_FIELDS)}")

        spec = QuerySpec(filters, search, sort_by, sort_dir, page, page_size)
        rows, total = self.product_dao.search(spec)
        items = [Product(r["id"], r["name"], r["description"], r["price"], r["stock"]) for r in rows]
        return PageResult(items, total, spec.page, spec.page_size)

    def bulk_upload(self, file_path, admin_full_name):
        import csv
        valid, errors = [], []
        try:
            with open(file_path, newline="") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader, start=2):  # row 1 = header
                    try:
                        name = row["name"].strip()
                        price = float(row["price"])
                        stock = int(row["stock"])
                        description = row.get("description", "").strip()
                        if not name:
                            raise ValueError("name is empty")
                        if price <= 0:
                            raise ValueError("price must be > 0")
                        if stock < 0:
                            raise ValueError("stock cannot be negative")
                        if self.product_dao.get_by_name(name):
                            raise ValueError(f"product '{name}' already exists, skipped")
                        valid.append((name, description, price, stock))
                    except (KeyError, ValueError) as e:
                        errors.append((i, str(e)))
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")

        inserted = self.product_dao.bulk_create(valid)
        log_action(f"Admin '{admin_full_name}' bulk uploaded {inserted} products ({len(errors)} rows failed)")
        return {"inserted": inserted, "failed": errors}