"""
InsightAI - Sample Business Data Generator

This module generates realistic business datasets
for the InsightAI Decision Intelligence Platform.

The generated datasets will be used for:
- SQL Analytics
- Dashboard Development
- Machine Learning
- Natural Language to SQL
- AI Reasoning
"""

import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

# Dataset configuration
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 50
NUM_ORDERS = 5000

# Sample customer data
MALE_NAMES = [
    "Raunak", "Ansh", "Arnav", "Ratan", "Vishu",
    "Adi", "Hans", "Purav", "Satvik", "Akshat"
]

FEMALE_NAMES = [
    "Pakhi", "Samantha", "Natasha", "Rim", "Poorna",
    "Kiara", "Avni", "Sanvi", "Varsha", "Urvashi"
]

GENDERS = [
    "Male",
    "Female"
]

CITIES = [
    ("Noida", "Uttar Pradesh"),
    ("Delhi", "Delhi"),
    ("Jaipur", "Rajasthan"),
    ("Lucknow", "Uttar Pradesh"),
    ("Chandigarh", "Chandigarh"),
    ("Mumbai", "Maharashtra"),
    ("Pune", "Maharashtra"),
    ("Bengaluru", "Karnataka"),
    ("Hyderabad", "Telangana"),
    ("Chennai", "Tamil Nadu")
]

PRODUCTS = {
    "Electronics": [
        "Laptop",
        "Smartphone",
        "Headphones",
        "Keyboard",
        "Mouse",
        "Monitor",
        "Tablet",
        "Smartwatch"
    ],
    "Clothing": [
        "T-Shirt",
        "Jeans",
        "Jacket",
        "Shoes",
        "Hoodie",
        "Cap"
    ],
    "Grocery": [
        "Rice",
        "Milk",
        "Bread",
        "Sugar",
        "Tea",
        "Coffee"
    ],
    "Books": [
        "Python Programming",
        "SQL Basics",
        "Data Science",
        "Machine Learning",
        "AI Fundamentals"
    ],
    "Home": [
        "Chair",
        "Table",
        "Lamp",
        "Bottle",
        "Fan"
    ]
}

def generate_customers():
    """Generate customer data and save it to customers.csv."""

    output_file = Path("data/customers.csv")

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "customer_id",
            "customer_name",
            "age",
            "gender",
            "city",
            "state"
        ])

        for i in range(1, NUM_CUSTOMERS + 1):
            customer_id = f"C{i:03}"

            gender = random.choice(GENDERS)

            if gender == "Male":
                customer_name = random.choice(MALE_NAMES)
            else:
                customer_name = random.choice(FEMALE_NAMES)

            age = random.randint(18, 65)

            city, state = random.choice(CITIES)

            writer.writerow([
                customer_id,
                customer_name,
                age,
                gender,
                city,
                state
            ])

    print(f"Customer data saved to: {output_file}")

def generate_product_prices():
    """Generate a price for each product ID."""

    prices = {}

    for i in range(1, NUM_PRODUCTS + 1):
        product_id = f"P{i:03}"
        prices[product_id] = round(random.uniform(100, 50000), 2)

    return prices

def generate_products():
    """Generate product data and save it to products.csv."""

    output_file = Path("data/products.csv")

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "product_id",
            "product_name",
            "category",
            "price",
            "inventory_level"
        ])

        for i in range(1, NUM_PRODUCTS + 1):
            product_id = f"P{i:03}"

            category = random.choice(list(PRODUCTS.keys()))
            product_name = random.choice(PRODUCTS[category])

            price = round(random.uniform(100, 50000), 2)

            inventory_level = random.randint(0, 500)

            writer.writerow([
                product_id,
                product_name,
                category,
                price,
                inventory_level
            ])

    print(f"Product data saved to: {output_file}")

def generate_orders():
    """Generate order data and save it to orders.csv."""

    output_file = Path("data/orders.csv")

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "order_id",
            "customer_id",
            "product_id",
            "order_date",
            "quantity",
            "total_amount"
        ])

        product_prices = generate_product_prices()
        start_date = datetime(2025, 1, 1)

        for i in range(1, NUM_ORDERS + 1):
            order_id = f"O{i:03}"

            customer_id = f"C{random.randint(1, NUM_CUSTOMERS):03}"
            product_id = f"P{random.randint(1, NUM_PRODUCTS):03}"

            days = random.randint(0, 364)
            order_date = (
                start_date + timedelta(days=days)
            ).strftime("%Y-%m-%d")

            quantity = random.randint(1, 5)
            price = product_prices[product_id]
            total_amount = round(price * quantity, 2)

            writer.writerow([
                order_id,
                customer_id,
                product_id,
                order_date,
                quantity,
                total_amount
            ])

    print(f"Order data saved to: {output_file}")

def main():
    """Main entry point for generating all business datasets."""
    print("Starting InsightAI data generation...")

    generate_customers()
    generate_products()
    generate_orders()


if __name__ == "__main__":
    main()