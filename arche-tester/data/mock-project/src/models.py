"""Data models for the mock project.

Contains Pydantic models for users, products, and orders.
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    """User roles in the system."""

    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class User(BaseModel):
    """User model."""

    id: int
    username: str
    email: str
    role: UserRole = UserRole.USER
    created_at: datetime = Field(default_factory=datetime.now)

    # TODO: Add password hashing
    # TODO: Add email validation


class Product(BaseModel):
    """Product model."""

    id: int
    name: str
    description: str
    price: float
    stock: int = 0

    def is_available(self) -> bool:
        """Check if product is in stock."""
        return self.stock > 0


class OrderStatus(str, Enum):
    """Order status values."""

    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderItem(BaseModel):
    """Single item in an order."""

    product_id: int
    quantity: int
    unit_price: float

    @property
    def total(self) -> float:
        """Calculate item total."""
        return self.quantity * self.unit_price


class Order(BaseModel):
    """Order model."""

    id: int
    user_id: int
    items: list[OrderItem]
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)

    @property
    def total(self) -> float:
        """Calculate order total."""
        return sum(item.total for item in self.items)


# Duplicate validation function (intentional for anti-duplication tests)
def validate_email(email: str) -> bool:
    """Validate email format."""
    return "@" in email and "." in email.split("@")[1]


def validate_username(username: str) -> bool:
    """Validate username format."""
    return len(username) >= 3 and username.isalnum()
