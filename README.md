# Little Lemon API 🍋

A robust and secure RESTful backend API for the Little Lemon restaurant, built using **Django** and **Django REST Framework (DRF)**. This project serves as the capstone for the Meta Django Web Framework / APIs certification program.

The API supports user registration, token-based authentication, role-based access control (RBAC), menu item management, shopping cart operations, and an order dispatching system.

---

## 🚀 Features

- **User Authentication**: Token-based authentication using **Djoser**.
- **Role-Based Access Control (RBAC)**: Distinct permissions for Managers, Delivery Crew, and Customers.
- **Menu Management**: Categorized menu items with filtering, searching, and sorting capabilities.
- **Cart System**: Customer-specific shopping carts to stage items before order placement.
- **Order Management**: Order submission, manager assignment of orders to delivery crew, and delivery status updates.
- **Throttling & Pagination**: Protects server resources with rate limiting (5 requests/min) and supports clean page-by-page list endpoints.

---

## 🛠️ Tech Stack

- **Backend**: [Django](https://www.djangoproject.com/) & [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
- **Auth Provider**: [Djoser](https://djoser.readthedocs.io/)
- **Database**: SQLite3 (default, configurable)
- **Dependency Management**: Pipenv / requirements.txt

---

## 🔒 Permission & Access Matrix

The system implements strict permission checks based on three main roles: **Managers**, **Delivery Crew**, and regular **Customers**.

| Endpoint | HTTP Method | Manager | Delivery Crew | Customer | Anonymous |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`/auth/users/`** (Register) | `POST` | ✅ | ✅ | ✅ | ✅ |
| **`/auth/token/login/`** (Login) | `POST` | ✅ | ✅ | ✅ | ✅ |
| **`/api/menu-items`** | `GET` | ✅ | ✅ | ✅ | ✅ |
| **`/api/menu-items`** | `POST` | ✅ (Create) | ❌ | ❌ | ❌ |
| **`/api/menu-items/<id>`** | `GET` | ✅ | ✅ | ✅ | ✅ |
| **`/api/menu-items/<id>`** | `PUT`, `PATCH`, `DELETE` | ✅ | ❌ | ❌ | ❌ |
| **`/api/cart/menu-items`** | `GET`, `POST`, `DELETE` | ❌ | ❌ | ✅ (Own Cart) | ❌ |
| **`/api/orders`** | `GET` | ✅ (All Orders) | ✅ (Assigned) | ✅ (Own Orders) | ❌ |
| **`/api/orders`** | `POST` | ❌ | ❌ | ✅ (Place Order) | ❌ |
| **`/api/orders/<id>`** | `GET` | ✅ | ✅ (Assigned) | ✅ (Own Order) | ❌ |
| **`/api/orders/<id>`** | `PATCH` | ✅ (Assign Crew/Status) | ✅ (Status Only) | ❌ | ❌ |
| **`/api/orders/<id>`** | `DELETE` | ✅ | ❌ | ❌ | ❌ |
| **`/api/groups/manager/users`** | `GET`, `POST` | ✅ | ❌ | ❌ | ❌ |
| **`/api/groups/manager/users/<id>`**| `DELETE` | ✅ | ❌ | ❌ | ❌ |
| **`/api/groups/delivery-crew/users`**| `GET`, `POST` | ✅ | ❌ | ❌ | ❌ |
| **`/api/groups/delivery-crew/users/<id>`**| `DELETE` | ✅ | ❌ | ❌ | ❌ |

---

## 🚦 Getting Started

### Prerequisites
- Python 3.10+
- `pip` or `pipenv`

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/little-lemon-api.git
   cd little-lemon-api
   ```

2. **Set up virtual environment & Install dependencies**
   *Using pipenv (recommended):*
   ```bash
   pipenv install
   pipenv shell
   ```
   *Using standard venv & pip:*
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix/macOS:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

4. **Initialize User Groups**
   The RBAC system relies on Django Auth Groups. Run the following command in the Django shell to set up `Manager` and `Delivery crew` groups:
   ```bash
   python manage.py shell
   ```
   *Within the shell:*
   ```python
   from django.contrib.auth.models import Group
   Group.objects.get_or_create(name='Manager')
   Group.objects.get_or_create(name='Delivery crew')
   exit()
   ```

5. **Create a Superuser**
   To access the admin portal:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the local server**
   ```bash
   python manage.py runserver
   ```
   The API will now be running at `http://127.0.0.1:8000/`.

---

## ⚡ API Endpoint Guide

Always include the Authorization header for protected endpoints:
`Authorization: Token <your_token>`

### 1. Authentication
* **Register**: `POST /auth/users/` (Payload: `username`, `password`, `email`)
* **Login**: `POST /auth/token/login/` (Payload: `username`, `password`) - Returns auth token.
* **Logout**: `POST /auth/token/logout/` - Invalidates auth token.

### 2. Menu Items
* **List items**: `GET /api/menu-items`
  * *Supports filtering*: `/api/menu-items?category=1&price=15.00`
  * *Supports searching*: `/api/menu-items?search=pasta`
  * *Supports sorting*: `/api/menu-items?ordering=price` (asc) or `-price` (desc)
  * *Supports pagination*: `/api/menu-items?page=2` (page size = 2)
* **Create item (Manager only)**: `POST /api/menu-items` (Payload: `title`, `price`, `inventory`, `category_id`)
* **Modify item (Manager only)**: `PUT/PATCH /api/menu-items/<id>`
* **Delete item (Manager only)**: `DELETE /api/menu-items/<id>`

### 3. Cart Operations (Customers only)
* **Get cart**: `GET /api/cart/menu-items`
* **Add to cart**: `POST /api/cart/menu-items` (Payload: `menuitem`, `quantity`)
* **Clear cart**: `DELETE /api/cart/menu-items`

### 4. Orders
* **Get orders**: `GET /api/orders`
  * Customers see their own order history.
  * Delivery crew see orders assigned to them.
  * Managers see all orders.
* **Place order (Customer only)**: `POST /api/orders` (converts cart items to an order and clears the cart)
* **Assign crew & update status (Manager only)**: `PATCH /api/orders/<id>` (Payload: `delivery_crew` [User ID], `status` [0 or 1])
* **Update delivery status (Delivery crew only)**: `PATCH /api/orders/<id>` (Payload: `status` [0 or 1])
* **Delete order (Manager only)**: `DELETE /api/orders/<id>`

---

## 🤝 Contributing
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.