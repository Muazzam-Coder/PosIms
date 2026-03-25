# Point of Sale & Inventory Management System (2026 Edition)

A fully-featured, modern, keyboard-first Point of Sale (POS) and Inventory Management System built with **Django**. Optimized for high-throughput retail environments with premium UI/UX, built-in analytics, and a native REST API.

## 🚀 Key Features

### 💻 Modern POS Engine
- **Keyboard-First Workflow:** Navigate the entire checkout process without a mouse using `Mousetrap.js`. (e.g., `F2` to Search, `F4` to discount, `F8` checkout).
- **Lightning Search:** HTML5 datalist barcode/SKU scanner integration.
- **Smart Receipts:** One-click Email receipts or print optimized (`@media print`) layouts for 80mm thermal printers.

### 📊 Advanced Dashboards & Analytics
- **Role-Based Access Control:** Distinct views for `Admin`, `Manager`, and `Cashier` roles.
- **Visual Analytics:** Interactive `Chart.js` components tracking the last 7 days of revenue natively.
- **1-Click Exporting:** Instantly export sales history, product status, and inventory data out to `.csv` format.
- **Low Stock Alerts:** Automated warnings when inventory falls below threshold levels.

### 🔌 RESTful API Integration
- Exposes a clean API mapping for `Products`, `Sales`, `Customers`, and `Returns` via Django REST Framework.
- Endpoint Base: `http://localhost:8000/api/`

## 🛠️ Technology Stack
* **Backend:** Python 3, Django 5.x, Django REST Framework
* **Frontend:** Bootstrap 5, SweetAlert2, HTML5 Datalists
* **Libraries:** Chart.js (Analytics), JsBarcode (1D Barcode generation)
* **Database:** SQLite (default) / PostgreSQL-ready

---

## ⚙️ Installation & Setup

Follow these instructions to run the application locally in an isolated virtual environment.

### 1. Prerequisites
- Python 3.10+
- `pip` package manager

### 2. Standard Setup

Clone the repository and install the minimal dependencies:

```bash
# Move into the project directory
cd "Point of Sales and Inventory Management System/posIms"

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install strictly required dependencies
pip install -r requirements.txt
```

### 3. Database Initialization

Run the migrations to set up the SQLite database models:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create an Admin User

To access the Admin dashboard and manage staff:

```bash
python manage.py createsuperuser
```

### 5. Start the Application

```bash
python manage.py runserver 0.0.0.0:8000
```
Then navigate to `http://localhost:8000/` in your browser.

---

## ⌨️ POS Hotkeys Reference

| Action | Shortcut | Scope |
| :--- | :--- | :--- |
| **Search Products** | `F2` | Sales Dashboard |
| **Apply Discount** | `F4` | Sales Dashboard |
| **Complete Checkout** | `F8` | Sales Dashboard |
| **Cancel / Reset** | `Esc` | Sales Dashboard |

---

## 📖 API Documentation
If you intend to connect external apps (e.g., a Mobile Cashier App), authenticate and query the following interactive endpoints:
- `GET /api/products/` - List products
- `GET /api/sales/` - List sales
- `GET /api/customers/` - List customers

## 📄 License
This POS system was developed internally for custom retail use cases.
