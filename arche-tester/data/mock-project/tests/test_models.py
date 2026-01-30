"""Tests for data models."""

import pytest
from src.models import (
    Order,
    OrderItem,
    OrderStatus,
    Product,
    User,
    UserRole,
    validate_email,
    validate_username,
)


class TestUser:
    """Tests for User model."""

    def test_create_user(self) -> None:
        """Test basic user creation."""
        user = User(id=1, username="testuser", email="test@example.com")
        assert user.id == 1
        assert user.username == "testuser"
        assert user.role == UserRole.USER

    def test_admin_role(self) -> None:
        """Test admin user creation."""
        user = User(
            id=1,
            username="admin",
            email="admin@example.com",
            role=UserRole.ADMIN,
        )
        assert user.role == UserRole.ADMIN


class TestProduct:
    """Tests for Product model."""

    def test_product_available(self) -> None:
        """Test product availability check."""
        product = Product(
            id=1,
            name="Test Product",
            description="A test product",
            price=9.99,
            stock=10,
        )
        assert product.is_available() is True

    def test_product_out_of_stock(self) -> None:
        """Test out of stock product."""
        product = Product(
            id=1,
            name="Test Product",
            description="A test product",
            price=9.99,
            stock=0,
        )
        assert product.is_available() is False


class TestOrder:
    """Tests for Order model."""

    def test_order_total(self) -> None:
        """Test order total calculation."""
        items = [
            OrderItem(product_id=1, quantity=2, unit_price=10.0),
            OrderItem(product_id=2, quantity=1, unit_price=5.0),
        ]
        order = Order(id=1, user_id=1, items=items)
        assert order.total == 25.0

    def test_order_status_default(self) -> None:
        """Test default order status."""
        order = Order(id=1, user_id=1, items=[])
        assert order.status == OrderStatus.PENDING


class TestValidation:
    """Tests for validation functions."""

    def test_valid_email(self) -> None:
        """Test valid email validation."""
        assert validate_email("test@example.com") is True
        assert validate_email("user@domain.org") is True

    def test_invalid_email(self) -> None:
        """Test invalid email validation."""
        assert validate_email("invalid") is False
        assert validate_email("no-at-sign.com") is False

    def test_valid_username(self) -> None:
        """Test valid username validation."""
        assert validate_username("user123") is True
        assert validate_username("testuser") is True

    def test_invalid_username(self) -> None:
        """Test invalid username validation."""
        assert validate_username("ab") is False  # Too short
        assert validate_username("user-name") is False  # Invalid char
