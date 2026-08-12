import yaml
import random
import datetime
import json

with open("config.yml", "r") as f:
    data = yaml.safe_load(f)
    print(data)

def generate_order_id(data):
    existing_ids = {item["order_id"] for item in data}

    while True:
        new_id = random.randint(1, 100)
        if new_id not in existing_ids:
            return new_id

def generate_customer_id(data):
    existing_ids = {item["customer_id"] for item in data}

    while True:
        new_id = random.randint(1000, 9999)
        if new_id not in existing_ids:
            return new_id

def generate_random_product():
    product_list = ["Laptop","Mobile Phone","Monitor","Keyboard","Mouse","Headphones"]
    return random.choice(product_list)

def generate_order_date():
    year = 2026

    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)

    random_date = start_date + datetime.timedelta(
        days=random.randint(
            0,
            (end_date - start_date).days
        )
    )

    return random_date.strftime("%Y-%m-%d")

def main():

    orders = []

    try:
        n = int(input("Enter number of orders: "))

        if n <= 0:
            print("Number of orders must be greater than 0")
            return

    except ValueError:
        print("Please enter a valid number")
        return

    for i in range(n):

        order = {}

        order["order_id"] = generate_order_id(orders)
        order["customer_id"] = generate_customer_id(orders)
        order["product"] = generate_random_product()

        order["quantity"] = random.randint(1, 5)

        order["unit_price"] = round(
            random.uniform(
                data["minimum_order_amount"],
                data["maximum_order_amount"]
            ),
            2
        )

        order["total_amount"] = round(
            order["quantity"] * order["unit_price"],
            2
        )

        order["status"] = random.choice(
            data["allowed_statuses"]
        )

        order["order_date"] = generate_order_date()

        orders.append(order)

    # Write orders to JSON
    with open("orders.json", "w") as f:
        json.dump(orders, f, indent=4)

    # Read orders back from JSON
    with open("orders.json", "r") as f:
        orders = json.load(f)

    # Generate summary
    total_sales = sum(
        order["total_amount"] for order in orders
    )

    highest_order = max(
        order["total_amount"] for order in orders
    )

    lowest_order = min(
        order["total_amount"] for order in orders
    )

    delivered_orders = sum(
        1 for order in orders
        if order["status"] == "Delivered"
    )

    cancelled_orders = sum(
        1 for order in orders
        if order["status"] == "Cancelled"
    )

    print("\n==================================")
    print(f"{data['store_name']} Order Report")
    print("==================================")

    print(f"Total Orders     : {len(orders)}")
    print(f"Total Sales      : {data['default_currency']} {total_sales:,.2f}")
    print(f"Highest Order    : {data['default_currency']} {highest_order:,.2f}")
    print(f"Lowest Order     : {data['default_currency']} {lowest_order:,.2f}")
    print(f"Delivered Orders : {delivered_orders}")
    print(f"Cancelled Orders : {cancelled_orders}")

    print("Order data saved successfully.")


if __name__ == "__main__":
    main()