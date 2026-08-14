from config.database import execute_many, execute_query, execute_update
from src.models.product import Product

ALLOWED_SORT_FIELDS = {"name", "price", "stock", "created_at"}


class ProductDAO:
    def get_all(self):
        return execute_query("SELECT * FROM products")


    def get_by_id(self, product_id):
        results = execute_query("SELECT * FROM products WHERE id = %s", (product_id,))
        if not results:
            return None
        row = results[0]
        return Product(
            product_id=row["id"],
            name=row["name"],
            description=row["description"],
            price=row["price"],
            stock=row["stock"]
        )

    def get_by_name(self, name):
        results = execute_query("SELECT * FROM products WHERE name = %s", (name,))
        return results[0] if results else None

    def create(self, name, description, price, stock):
        product_id, _ = execute_update(
            "INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s)",
            (name, description, price, stock)
        )
        return product_id

    def update(self, product_id, fields_dict):
        if not fields_dict:
            return False
        updates = []
        params = []
        for k, v in fields_dict.items():
            updates.append(f"{k} = %s")
            params.append(v)
        params.append(product_id)
        
        query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
        _, affected = execute_update(query, tuple(params))
        return affected > 0

    def delete(self, product_id):
        _, affected = execute_update("DELETE FROM products WHERE id = %s", (product_id,))
        return affected > 0

    def update_stock(self, product_id, quantity):
        _, affected = execute_update(
            "UPDATE products SET stock = stock + %s WHERE id = %s",
            (quantity, product_id)
        )
        return affected > 0

    def search(self, spec):
        where_clauses, params = [], []

        if "price_min" in spec.filters:
            where_clauses.append("price >= %s")
            params.append(spec.filters["price_min"])
        if "price_max" in spec.filters:
            where_clauses.append("price <= %s")
            params.append(spec.filters["price_max"])
        if "stock_min" in spec.filters:
            where_clauses.append("stock >= %s")
            params.append(spec.filters["stock_min"])
        if spec.filters.get("in_stock"):
            where_clauses.append("stock > 0")
        if spec.search:
            where_clauses.append("(name LIKE %s OR description LIKE %s)")
            like = f"%{spec.search}%"
            params.extend([like, like])

        where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
        order_sql = f"ORDER BY {spec.sort_by} {spec.sort_dir}" if spec.sort_by in ALLOWED_SORT_FIELDS else ""

        total_row = execute_query(f"SELECT COUNT(*) as total FROM products {where_sql}", params)
        total = total_row[0]["total"] if total_row else 0

        query = f"SELECT * FROM products {where_sql} {order_sql} LIMIT %s OFFSET %s"
        rows = execute_query(query, params + [spec.page_size, spec.offset])
        return rows, total

    def bulk_create(self, rows):
        """rows: list of (name, description, price, stock) tuples."""
        if not rows:
            return 0
        query = "INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s)"
        return execute_many(query, rows)