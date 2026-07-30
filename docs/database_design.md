# Database Design

## Purpose

This document defines how the business entities of InsightAI will be represented as relational database tables.

A well-designed database ensures that business data is organised, consistent, and easy to query for analytics, machine learning, and AI applications.
---

## Entity to Table Mapping

| Business Entity | Database Table |
|-----------------|----------------|
| Customer | customers |
| Product | products |
| Order | orders |
| Supplier | suppliers |
| Inventory | inventory |
| Marketing Campaign | marketing_campaigns |
---

## Primary Keys

Each database table will have a unique Primary Key.

| Table | Primary Key |
|--------|-------------|
| customers | customer_id |
| products | product_id |
| orders | order_id |
| suppliers | supplier_id |
| inventory | inventory_id |
| marketing_campaigns | campaign_id |
---

## Foreign Keys

Foreign Keys connect one table to another by referencing the Primary Key of another table.

| Table | Foreign Key | References |
|--------|-------------|------------|
| orders | customer_id | customers.customer_id |
| orders | product_id | products.product_id |
| products | supplier_id | suppliers.supplier_id |
| inventory | product_id | products.product_id |
---

## Initial Entity Relationship Diagram (Conceptual)

Customer
│
└── places ─────► Order
                  │
                  └── contains ───► Product
                                      │
                                      ├── supplied by ─► Supplier
                                      │
                                      └── tracked in ─► Inventory

Marketing Campaign
        │
        └── influences ─► Order
---

## Common Data Types

| Data Type | Purpose | Example |
|-----------|---------|---------|
| INTEGER | Whole numbers | 25 |
| REAL | Decimal values | 199.99 |
| TEXT | Text values | Nishu |
| TEXT (Date Format: YYYY-MM-DD) | Dates | 2026-07-30 |
---

## Common Database Constraints

| Constraint | Purpose | Example |
|------------|---------|---------|
| PRIMARY KEY | Uniquely identifies each record | customer_id |
| NOT NULL | Prevents empty values | customer_name |
| UNIQUE | Prevents duplicate values | email |
| CHECK | Ensures valid values | age >= 0 |