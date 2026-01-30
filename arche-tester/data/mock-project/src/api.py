"""API endpoints for the mock project.

Contains HTTP handlers for users, products, and orders.
"""

from typing import Any

from src.models import Order, Product, User, UserRole


# In-memory storage (for testing)
_users: dict[int, User] = {}
_products: dict[int, Product] = {}
_orders: dict[int, Order] = {}


class APIError(Exception):
    """Base API error."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(APIError):
    """Resource not found."""

    def __init__(self, resource: str, id: int) -> None:
        super().__init__(f"{resource} {id} not found", 404)


class ValidationError(APIError):
    """Validation failed."""

    def __init__(self, field: str, message: str) -> None:
        super().__init__(f"{field}: {message}", 400)


# User endpoints
def get_user(user_id: int) -> User:
    """Get user by ID."""
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValidationError("user_id", "must be a positive integer")
    if user_id not in _users:
        raise NotFoundError("User", user_id)
    return _users[user_id]


def create_user(data: dict[str, Any]) -> User:
    """Create new user."""
    from src.models import validate_email, validate_username

    # Validate required fields
    if "username" not in data:
        raise ValidationError("username", "is required")
    if "email" not in data:
        raise ValidationError("email", "is required")

    # Validate username format
    if not validate_username(data["username"]):
        raise ValidationError("username", "must be at least 3 alphanumeric characters")

    # Validate email format
    if not validate_email(data["email"]):
        raise ValidationError("email", "invalid format")

    user_id = len(_users) + 1
    user = User(id=user_id, **data)
    _users[user_id] = user
    return user


def list_users(role: UserRole | None = None) -> list[User]:
    """List all users, optionally filtered by role."""
    users = list(_users.values())
    if role:
        users = [u for u in users if u.role == role]
    return users


# Product endpoints
def get_product(product_id: int) -> Product:
    """Get product by ID."""
    if not isinstance(product_id, int) or product_id <= 0:
        raise ValidationError("product_id", "must be a positive integer")
    if product_id not in _products:
        raise NotFoundError("Product", product_id)
    return _products[product_id]


def create_product(data: dict[str, Any]) -> Product:
    """Create new product."""
    product_id = len(_products) + 1
    product = Product(id=product_id, **data)
    _products[product_id] = product
    return product


def list_products(in_stock_only: bool = False) -> list[Product]:
    """List all products."""
    products = list(_products.values())
    if in_stock_only:
        products = [p for p in products if p.is_available()]
    return products


# Order endpoints
def get_order(order_id: int) -> Order:
    """Get order by ID."""
    if not isinstance(order_id, int) or order_id <= 0:
        raise ValidationError("order_id", "must be a positive integer")
    if order_id not in _orders:
        raise NotFoundError("Order", order_id)
    return _orders[order_id]


def create_order(user_id: int, items: list[dict[str, Any]]) -> Order:
    """Create new order."""
    # Validate user exists
    get_user(user_id)

    # Validate products exist and have stock
    from src.models import OrderItem

    order_items = []
    for item_data in items:
        product = get_product(item_data["product_id"])
        if not product.is_available():
            raise ValidationError("product", f"Product {product.id} is out of stock")
        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=item_data["quantity"],
                unit_price=product.price,
            )
        )

    order_id = len(_orders) + 1
    order = Order(id=order_id, user_id=user_id, items=order_items)
    _orders[order_id] = order
    return order


def list_orders(user_id: int | None = None) -> list[Order]:
    """List orders, optionally filtered by user."""
    orders = list(_orders.values())
    if user_id:
        orders = [o for o in orders if o.user_id == user_id]
    return orders
