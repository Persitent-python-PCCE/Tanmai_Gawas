import csv
from collections import defaultdict
import statistics

report_product = defaultdict(int)
report_category = defaultdict(int)
all_transactions = []  

with open("sales.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        revenue = int(row["quantity"]) * int(row["unit_price"])
        product_name = row["product"]
        category_name = row["category"]
        
        report_product[product_name] += revenue
        report_category[category_name] += revenue
        
        all_transactions.append(revenue)

total_revenue = sum(all_transactions)
avg_per_txn = statistics.mean(all_transactions)

top_product_name, top_product_revenue = max(report_product.items(), key=lambda x: x[1])

print("=== Sales Report ===")
print("Revenue by Category:")
for category, rev in report_category.items():
    print(f" {category} : {float(rev):.2f}")

print(f"Top Product : {top_product_name} ({float(top_product_revenue):.2f})")
print(f"Total Revenue : {float(total_revenue):.2f}")
print(f"Avg / Txn : {float(avg_per_txn):.2f}")
