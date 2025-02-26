# Point of Sales (POS) API

## Introduction
This project is a FastAPI-based service for a Point of Sales (POS) system. It provides an HTTP API for managing store products, applying promotional campaigns, handling receipts, and generating reports.

## Features
- Product registration and price management
- Promotional campaigns: "buy_n_get_n", "discount", and "combo"
- Receipt management with item addition and payment handling
- Reporting: shift reports (X Reports) and lifetime sales reports
- Multi-currency payment support (GEL, USD, EUR)

## User Stories
### Store Manager
- Register goods and their prices
- View and update product listings
- Create and manage promotional campaigns
- Generate reports to track sales and shifts

### Cashier
- Open and close shifts
- Handle receipts: create, add items, calculate totals, and process payments

### Customer
- Receive detailed receipts with discounts and total payment
- Pay using different currencies (GEL, USD, EUR)


## Campaign Types
### Discount
- Discounts can be applied to specific items if a threshold is met.
- campaign_type `discount`  

**Example Request:**
```json
{
  "discount_percentage": 20,
  "applicable_product": "1"
}
```

### Buy N Get N
- Customers receive free items when purchasing a certain quantity of a specific product.
- campaign_type `buy_n_get_n`  

**Example Request:**
```json
{
  "required_quantity": 2,
  "product_id": "1"
}
```

### Combo
- Discounts are applied when specific products are purchased together.
- campaign_type `combo`  

**Example Request:**
```json
{
  "product_ids": ["1", "2"],
  "discount_percentage": 10
}
```

## Payment System
- Base currency: GEL
- Conversion to USD and EUR via a public exchange rate API

## Reports
### X Report
- Number of receipts in the shift
- Total items sold (by product ID)
- Revenue breakdown by currency

### Sales Report
- Lifetime sales summary by currency

## Technical Stack
- **Framework**: FastAPI
- **Database**: SQLite (for persistence)
- **Authorization**: Not required (all API endpoints are unrestricted)
- **Linting & Formatting**: `ruff` for code formatting, `mypy` for static type checking

## API Endpoints
### Products
- **Create a product**: `POST /products`
- **List products**: `GET /products`
- **Update product details**: `PATCH /products/{product_id}`

### Campaigns
- **Create a campaign**: `POST /campaigns`
- **Deactivate a campaign**: `DELETE /campaigns/{campaign_id}`
- **List all campaigns**: `GET /campaigns`

### Receipts
- **Create a receipt**: `POST /receipts`
- **Add items to a receipt**: `POST /receipts/{receipt_id}/products`
- **Calculate total payment in a specific currency**: `POST /receipts/{receipt_id}/quotes`
- **Process a payment for a receipt**: `POST /receipts/{receipt_id}/payments`

### Reports
- **Fetch an X Report for an open shift**: `GET /x-reports?shift_id={shift_id}`
- **Fetch a lifetime sales report**: `GET /sales`



