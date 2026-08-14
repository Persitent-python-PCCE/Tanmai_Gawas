class Cart:
    def __init__(self):
        self._items = {}
        self._products = {}

    def add_item(self, product, quantity=1):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        
        current_qty = self._items.get(product.product_id, 0)
        new_qty = current_qty + quantity
        
        if product.stock < new_qty:
            raise ValueError(
                f"Insufficient stock for '{product.name}'. Available: {product.stock}"
            )
        self._items[product.product_id] = new_qty
        self._products[product.product_id] = product

    def remove_item(self, product_id, quantity=None):
        if product_id not in self._items:
            raise ValueError("Product not in cart.")
        
        if quantity is None or quantity >= self._items[product_id]:
            del self._items[product_id]
            if product_id in self._products:
                del self._products[product_id]
        else:
            if quantity <= 0:
                raise ValueError("Quantity to remove must be greater than zero.")
            self._items[product_id] -= quantity

    def clear(self):
        self._items.clear()
        self._products.clear()

    @property
    def items(self):
        return self._items

    def get_total_price(self):
        total = 0.0
        for pid, qty in self._items.items():
            prod = self._products.get(pid)
            if prod:
                total += float(prod.price) * qty
        return total

    def get_summary(self):
        summary = []
        for pid, qty in self._items.items():
            prod = self._products.get(pid)
            if prod:
                summary.append({
                    "product": prod,
                    "quantity": qty,
                    "subtotal": float(prod.price) * qty
                })
        return summary

    def get_item(self, product_id):
        return self._items.get(product_id)