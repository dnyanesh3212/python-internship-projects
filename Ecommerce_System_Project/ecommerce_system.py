#!/usr/bin/env python3
"""
Enhanced Simple E-commerce System (Internship Project)
------------------------------------------------------
Features:
- Products stored in products.csv
- Customers in customers.csv
- Sales recorded in sales.csv
- Customer registration & login
- Discounts with coupon codes
- Stock alerts when low
- Sales reports with ASCII charts
- Role-based menu (Customer / Admin)
"""

import csv
import os
import sys

products_file = "products.csv"
customers_file = "customers.csv"
sales_file = "sales.csv"

# Default coupons
coupons = {"SAVE10": 0.10, "SAVE20": 0.20}
stock_alert_threshold = 5

# ----------------- File Handling -----------------
def load_products():
    products = {}
    if os.path.exists(products_file):
        with open(products_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                products[int(row["id"])] = {
                    "name": row["name"],
                    "price": float(row["price"]),
                    "stock": int(row["stock"]),
                }
    else:
        # Default if missing
        products = {
            1: {"name": "Laptop", "price": 800, "stock": 10},
            2: {"name": "Smartphone", "price": 500, "stock": 15},
            3: {"name": "Headphones", "price": 150, "stock": 20},
            4: {"name": "Smartwatch", "price": 200, "stock": 12},
        }
        save_products(products)
    return products

def save_products(products):
    with open(products_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "price", "stock"])
        for pid, info in products.items():
            writer.writerow([pid, info["name"], info["price"], info["stock"]])

def load_customers():
    customers = {}
    if os.path.exists(customers_file):
        with open(customers_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                customers[row["username"]] = {
                    "name": row["name"],
                    "role": row.get("role", "customer"),  # role defaults to customer
                }
    return customers

def save_customers(customers):
    with open(customers_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["username", "name", "role"])
        for username, data in customers.items():
            writer.writerow([username, data["name"], data["role"]])

def load_sales():
    sales = []
    if os.path.exists(sales_file):
        with open(sales_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                sales.append({
                    "username": row["username"],
                    "product": row["product"],
                    "quantity": int(row["quantity"]),
                    "total": float(row["total"]),
                })
    return sales

def save_sales(sales):
    with open(sales_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["username", "product", "quantity", "total"])
        for sale in sales:
            writer.writerow([sale["username"], sale["product"], sale["quantity"], sale["total"]])

# ----------------- Core Functions -----------------
def display_products(products):
    print("\nAvailable Products:")
    print("ID | Product      | Price($) | Stock")
    print("--------------------------------------")
    for pid, info in products.items():
        alert = " (LOW STOCK!)" if info["stock"] <= stock_alert_threshold else ""
        print(f"{pid}  | {info['name']:<12} | {info['price']:<8.2f} | {info['stock']}{alert}")

def register_customer(customers):
    username = input("Choose a username: ").strip()
    if username in customers:
        print("❌ Username already exists!")
        return None
    name = input("Enter your full name: ").strip()
    role = "admin" if username.lower() == "admin" else "customer"
    customers[username] = {"name": name, "role": role}
    save_customers(customers)
    print(f"✅ Customer {name} registered successfully as {role}.")
    return username

def login_customer(customers):
    username = input("Enter your username: ").strip()
    if username in customers:
        print(f"👋 Welcome back, {customers[username]['name']} ({customers[username]['role']})!")
        return username
    else:
        print("❌ Username not found. Please register first.")
        return None

def apply_coupon():
    code = input("Enter discount coupon code (or press Enter to skip): ").strip().upper()
    if code in coupons:
        discount = coupons[code]
        print(f"🎉 Coupon applied! You get a {int(discount*100)}% discount.")
        return discount
    else:
        if code:
            print("❌ Invalid coupon code.")
        return 0.0

def purchase_product(products, username, sales):
    display_products(products)
    try:
        pid = int(input("\nEnter Product ID to purchase (0 to cancel): "))
        if pid == 0:
            return
        if pid not in products:
            print("❌ Invalid Product ID.")
            return
        qty = int(input("Enter quantity: "))
        if qty <= 0:
            print("❌ Quantity must be positive.")
            return
        if qty > products[pid]["stock"]:
            print("❌ Not enough stock available.")
            return
        discount = apply_coupon()
        total_cost = products[pid]["price"] * qty * (1 - discount)
        print(f"💵 Total cost after discount: ${total_cost:.2f}")
        confirm = input("Confirm purchase? (y/n): ").lower()
        if confirm == "y":
            products[pid]["stock"] -= qty
            sales.append({"username": username, "product": products[pid]["name"], "quantity": qty, "total": total_cost})
            save_products(products)
            save_sales(sales)
            print("✅ Purchase successful!")
            if products[pid]["stock"] <= stock_alert_threshold:
                print(f"⚠️ Alert: Stock for {products[pid]['name']} is low ({products[pid]['stock']})!")
        else:
            print("❌ Purchase cancelled.")
    except ValueError:
        print("❌ Invalid input. Please enter numbers only.")

def show_sales_report(sales):
    if not sales:
        print("\n📊 No sales made yet.")
        return
    print("\n📊 Sales Report")
    print("Product      | Quantity | Total Sales($)")
    print("-----------------------------------------")
    summary = {}
    revenue_by_customer = {}
    for sale in sales:
        summary.setdefault(sale["product"], {"quantity": 0, "total": 0})
        summary[sale["product"]]["quantity"] += sale["quantity"]
        summary[sale["product"]]["total"] += sale["total"]
        revenue_by_customer.setdefault(sale["username"], 0)
        revenue_by_customer[sale["username"]] += sale["total"]

    grand_total = 0
    for product, data in summary.items():
        bar = "#" * (data["quantity"] // 2)
        print(f"{product:<12} | {data['quantity']:<8} | ${data['total']:.2f} {bar}")
        grand_total += data["total"]

    print("-----------------------------------------")
    print(f"💰 Total Revenue: ${grand_total:.2f}")
    print(f"👥 Total Customers: {len(revenue_by_customer)}")
    top_customer = max(revenue_by_customer, key=revenue_by_customer.get)
    print(f"🏆 Top Customer: {top_customer} (${revenue_by_customer[top_customer]:.2f})")

def restock_products(products):
    print("\n🔄 Restock Products")
    display_products(products)
    try:
        pid = int(input("\nEnter Product ID to restock (0 to cancel): "))
        if pid == 0:
            return
        if pid not in products:
            print("❌ Invalid Product ID.")
            return
        qty = int(input("Enter quantity to add: "))
        if qty <= 0:
            print("❌ Quantity must be positive.")
            return
        products[pid]["stock"] += qty
        save_products(products)
        print(f"✅ Restocked {products[pid]['name']} by {qty} units.")
    except ValueError:
        print("❌ Invalid input. Please enter numbers only.")

# ----------------- Main CLI -----------------
def main():
    print("=" * 50)
    print("     🛒 Simple E-commerce System (CLI)     ")
    print("=" * 50)

    products = load_products()
    customers = load_customers()
    sales = load_sales()

    username = None
    while True:
        print("\n1. Register")
        print("2. Login")
        print("0. Exit")
        if username:
            role = customers[username]["role"]
            print(f"\nLogged in as: {username} ({role})")
            print("3. Show Products")
            print("4. Purchase Product")
            if role == "admin":
                print("5. Show Sales Report")
                print("6. Restock Products")
            print("7. Logout")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            username = register_customer(customers)
        elif choice == "2":
            username = login_customer(customers)
        elif choice == "3" and username:
            display_products(products)
        elif choice == "4" and username:
            purchase_product(products, username, sales)
        elif choice == "5" and username and customers[username]["role"] == "admin":
            show_sales_report(sales)
        elif choice == "6" and username and customers[username]["role"] == "admin":
            restock_products(products)
        elif choice == "7" and username:
            print(f"👋 User {username} logged out.")
            username = None
        elif choice == "0":
            print("👋 Exiting system. Goodbye!")
            sys.exit()
        else:
            print("❌ Invalid option or please login first.")

if __name__ == "__main__":
    main()
