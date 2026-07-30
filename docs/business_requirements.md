# Business Requirements

## Project Vision

InsightAI is an AI-powered Decision Intelligence Platform designed to help business users make informed decisions using structured data, unstructured business documents, and machine learning predictions.

The platform allows users to ask business questions in natural language and receive data-driven insights, visualisations, forecasts, and recommendations.
---

## Core Business Entities

The primary business entities used by InsightAI are:

### 1. Customer

Represents the people who purchase products from the business.

### 2. Product

Represents the items sold by the company.

### 3. Order

Represents a customer's purchase transaction.

### 4. Supplier

Represents vendors that supply products to the business.

### 5. Inventory

Represents stock available in warehouses.

### 6. Marketing Campaign

Represents promotional campaigns used to increase sales.
---

## Business Entity Attributes

### Customer

- Customer ID
- Name
- Age
- Gender
- City
- State

### Product

- Product ID
- Product Name
- Category
- Price
- Supplier
- Inventory Level

### Order

- Order ID
- Customer ID
- Product ID
- Quantity
- Revenue
- Profit
- Order Date

### Supplier

- Supplier ID
- Supplier Name
- Contact Name
- Delivery Time

### Inventory

- Inventory ID
- Warehouse
- Stock Quantity
- Last Updated

### Marketing Campaign

- Campaign ID
- Campaign Name
- Budget
- Clicks
- Conversions
- ROI
---

## Business Relationships

- A Customer places one or more Orders.
- An Order contains one or more Products.
- A Product is supplied by one Supplier.
- A Supplier supplies multiple Products.
- A Product has Inventory information.
- Marketing Campaigns influence Orders and Sales.
---

## Key Business Questions

InsightAI should be able to answer the following business questions:

1. Which products generated the highest revenue during a selected time period?

2. Why did sales decrease in a particular month?

3. What are the predicted sales for the next month?

4. Which customers are most likely to stop purchasing?

5. What actions should management take to improve revenue?
---

## Data Sources

InsightAI will use three primary categories of business data:

### 1. Structured Data
- Customer information
- Product information
- Orders
- Inventory
- Marketing campaigns

**Purpose:** Used for SQL analytics, KPIs, dashboards, and reporting.

### 2. Unstructured Data
- Customer complaints
- Sales meeting notes
- Supplier reports
- Marketing reports
- Product reviews
- Internal announcements

**Purpose:** Used by the RAG system to retrieve supporting evidence and business context.

### 3. Historical Business Data
- Historical sales
- Customer purchase history
- Inventory history
- Marketing performance

**Purpose:** Used to train machine learning models for forecasting, churn prediction, demand prediction, and anomaly detection.