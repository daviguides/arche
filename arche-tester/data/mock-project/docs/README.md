# Mock Project

A sample e-commerce API project for testing purposes.

## Structure

```
src/
├── models.py    # Data models (User, Product, Order)
├── api.py       # API endpoints
├── auth.py      # Authentication
└── utils.py     # Utility functions

tests/
└── test_models.py

config/
└── settings.yaml
```

## Models

### User

- `id`: Unique identifier
- `username`: Login name
- `email`: Email address
- `role`: USER, ADMIN, or GUEST

### Product

- `id`: Unique identifier
- `name`: Product name
- `price`: Unit price
- `stock`: Available quantity

### Order

- `id`: Unique identifier
- `user_id`: Owner
- `items`: List of OrderItems
- `status`: PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED

## API Endpoints

- `GET /users` - List users
- `POST /users` - Create user
- `GET /products` - List products
- `POST /products` - Create product
- `GET /orders` - List orders
- `POST /orders` - Create order

## Authentication

Sessions are stored in memory. Use `POST /login` with username/password.

## Configuration

See `config/settings.yaml` for all options.
