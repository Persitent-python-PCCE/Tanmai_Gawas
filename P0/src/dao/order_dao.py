from config.database import execute_query, get_connection

ALLOWED_ORDER_SORT_FIELDS = {"order_date", "total_price"}

class OrderDAO:
    def get_orders_by_user_id(self, user_id):
        return execute_query(
            "SELECT * FROM orders WHERE user_id = %s ORDER BY order_date DESC",
            (user_id,)
        )

    def get_order_items_by_order_id(self, order_id):
        return execute_query(
            "SELECT oi.*, p.name as product_name FROM order_items oi INNER JOIN products p ON oi.product_id = p.id WHERE oi.order_id = %s",
            (order_id,))

    def get_all_orders(self):
        return execute_query(
            "SELECT o.*, u.full_name FROM orders o INNER JOIN users u ON o.user_id = u.id ORDER BY o.order_date DESC"
        )

    def place_order_transaction(self, user_id, total_price, items):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO orders (user_id, total_price) VALUES (%s, %s)",
                (user_id, total_price)
            )
            order_id = cursor.lastrowid

            for item in items:
                pid = item['product_id']
                qty = item['quantity']
                price = item['price']

                cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price) "
                    "VALUES (%s, %s, %s, %s)",
                    (order_id, pid, qty, price)
                )

                cursor.execute(
                    "UPDATE products SET stock = stock - %s WHERE id = %s",
                    (qty, pid)
                )
            
            conn.commit()
            return order_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def search_orders(self, spec):
        where_clauses, params = [], []

        if "date_from" in spec.filters:
            where_clauses.append("o.order_date >= %s")
            params.append(spec.filters["date_from"])
        if "date_to" in spec.filters:
            where_clauses.append("o.order_date <= %s")
            params.append(spec.filters["date_to"])
        if "total_min" in spec.filters:
            where_clauses.append("o.total_price >= %s")
            params.append(spec.filters["total_min"])
        if "total_max" in spec.filters:
            where_clauses.append("o.total_price <= %s")
            params.append(spec.filters["total_max"])
        if spec.search:
            where_clauses.append("u.full_name LIKE %s")
            params.append(f"%{spec.search}%")

        where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
        order_sql = f"ORDER BY o.{spec.sort_by} {spec.sort_dir}" if spec.sort_by in ALLOWED_ORDER_SORT_FIELDS else "ORDER BY o.order_date DESC"

        count_query = f"""
            SELECT COUNT(*) as total FROM orders o
            INNER JOIN users u ON o.user_id = u.id
            {where_sql}
        """
        total_row = execute_query(count_query, params)
        total = total_row[0]["total"] if total_row else 0

        query = f"""
            SELECT o.*, u.full_name FROM orders o
            INNER JOIN users u ON o.user_id = u.id
            {where_sql}
            {order_sql}
            LIMIT %s OFFSET %s
        """
        rows = execute_query(query, params + [spec.page_size, spec.offset])
        return rows, total