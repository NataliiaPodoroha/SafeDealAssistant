# SafeDealAssistant

## A Project for Secure Transaction Facilitation

SafeDealAssistant is a Telegram bot designed to facilitate secure deals between buyers and sellers of digital goods (accounts, files, etc.). The bot automates deal creation, notifications, and management while ensuring a smooth experience for all parties involved.

___

## Table of Contents
- [Features](#features)
- [How the Service Works](#how-the-service-works)
- [Roles](#roles)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Fields of Improvement](#fields-of-improvement)

## Features

**Users:**

- **View Product Catalog:**
  - Access a catalog of products added by the administrator.
  - View detailed product information.

- **Create Deals:**
  - Initiate a deal as either a buyer or a seller.
  - Create deals even for products not listed in the catalog.

- **Accept or Decline Deals:**
  - The second party of the deal (specified during its creation) can accept or decline the deal.

**Administrator:**

- **Manage Product Catalog:**
  - Add, update, and delete products in the catalog.

- **View Deals:**
  - Access a list of all created deals.

- **Change Deal Status:**
  - Modify deal statuses to "Completed" or "Rejected."

- **Oversee Payments and Goods Transfer:**
  - Handle all financial transactions and the transfer of goods manually.

- **SimpleSwap Integration:**
  - Generate payment links via SimpleSwap after deal confirmation.
  - Support the deal currency for conversion to the administrator's wallet currency.

___

## How the Service Works

### 1. Product Catalog

Accessible to all users. Users can view:

- Product name.
- Price.
- Description.
- Seller's contact details.

The catalog is populated exclusively by the administrator through the admin panel.

___

### 2. Deal Creation Process

- User selects the "Create Deal" button.
- Chooses the type of deal:
  - "Buy" – the user wants to buy a product.
  - "Sell" – the user wants to sell a product.
- Enters details in the following format:

```mathematica
Product Name|Price|Currency|Other Party Username
```
- The bot creates a deal with the status "NEW" and notifies the second party.
- The second party can:
  - **Accept the deal ("Accept"):**
    - The status changes to "Accepted."
    - A payment link is generated via SimpleSwap.
    - The buyer receives the payment link.
    - The administrator is notified about the confirmed deal.
  - **Decline the deal ("Decline"):**
    - The status changes to "Declined."
    - The deal creator is notified about the rejection.

___

### 3. Administration of the Deal

The administrator receives a notification about the confirmed deal:

- Product name.
- Price.
- Buyer.
- Seller.

The administrator oversees payment and goods transfer:

- Contacts the seller to collect the goods.
- Verifies the payment on their wallet.
- Upon successful verification:
  - Transfers the goods to the buyer.
  - Transfers the payment to the seller.

___

### 4. Managing Deals via Admin Panel

The admin panel includes a "View Deals" section. The administrator can change deal statuses to:

- "Completed" – deal successfully closed.
- "Rejected" – deal canceled.

___

## Roles

**Users**

- Can create deals, accept or decline deals.
- Do not have access to the admin panel.

**Administrator**

- The sole user with permissions to:
  - Manage the product catalog.
  - View all deals.
  - Change deal statuses.
  - Oversee payment and goods transfer.

___

## How SimpleSwap Works

After deal confirmation, the bot generates a request to the SimpleSwap API. The request includes:

- Deal currency (`currency_from`).
- Administrator's wallet currency (`currency_to`).
- Deal amount (`amount`).
- Administrator's wallet address (`address_to`).

SimpleSwap returns a payment link, which is sent to the buyer.

___

## Interaction via Telegram

**Users**

Available commands:

- `/start` – begin interaction with the bot.
- `/catalog` – view the product catalog.
- `/create_deal` – initiate a deal.

**Administrator**

Access the admin panel via the command:

- `/admin`.

___

## Manual Steps for Finalizing the Deal

After the deal is confirmed, the administrator:

- Verifies the payment on their wallet.
- Collects the goods from the seller.
- Upon successful verification:
  - Transfers the goods to the buyer.
  - Transfers the payment to the seller.
- If either party fails to comply:
  - The administrator cancels the deal by changing its status to "Rejected."
  
___

## Setup Instructions

Clone the repository:

```bash
git clone https://github.com/username/SafeDealAssistant.git
```

Create a .env file with the following parameters:
```mathematica
BOT_TOKEN=YOUR_BOT_TOKEN
ADMIN_ID=YOUR_ADMIN_ID
DATABASE_URL=YOUR_DATABASE_URL
SIMPLE_SWAP_API_KEY=YOUR_SIMPLE_SWAP_API_KEY
ADMIN_WALLET_ADDRESS=A_VALID_WALLET_ADDRESS
ADMIN_WALLET_CURRENCY=A_VALID_WALLET_CURRENCY
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Initialize the database:
```bash
alembic upgrade head
```

Run the bot:
```bash
python run_bot.py
```
___

## Fields of Improvement

#### Finalizing Deals:
- Implement functionality for finalizing a deal when the administrator confirms the process is complete.
- Send a final notification to both parties about the successful completion of the deal.

#### Viewing Deal History:
- Add a feature allowing users to view the history of their deals.

#### Optimizing Notifications:
- Improve the formatting of notifications to make them more structured and professional.

#### Admin Action Logging
- Record all actions performed by the administrator (e.g., changing deal status, creating a product) in the database.
- Add an AdminLogs table to the database.

#### Input Data Validation
- Validate the format of user-inputted data during deal creation.
- Ensure amounts, currencies, and usernames are in the correct form