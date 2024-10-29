# Demo E-commerce App - Orders Service

This project demonstrates a simple e-commerce system built using a microservices architecture. It consists of one of the service used by this demo app:

**Order Processing Service**: Manages orders, including placing new orders and retrieving user order history.

## Technology Stack

- Backend: Flask (Python)
- Database: MySQL
- Authentication: JWT

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.12+
- Docker and Docker Compose (optional, for containerized deployment)

### Installation

1. **Set up virtual environment (optional)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. **Install dependencies**

Navigate to each service directory and install the required Python packages.

```bash
pip install -r requirements.txt
```

### Running the Services

#### Without Docker

Run the below command from the root path of the dir

```bash
export FLASK_APP='src/app.py'
export DATABASE_URL="mysql+pymysql://username:password@hostname:3306/defaultdb"
export PRODUCT_SERVICE_URL='http://localhost:5101'
flask run --port=5000
```

> The application should be up and running on http://127.0.0.1:5000


#### With Docker

Run the below command from root path of the dir

```bash
export DATABASE_URL="mysql+pymysql://username:password@hostname:3306/defaultdb"
export PRODUCT_SERVICE_URL='http://localhost:5101'
export USER_SERVICE_URL='http://localhost:5100'
docker build -t ecomm-order-service .
docker run -e DATABASE_URL=$DATABASE_URL -e PRODUCT_SERVICE_URL=$PRODUCT_SERVICE_URL -p 5000:5000 ecomm-order-service
```

> The application should be up and running on http://127.0.0.1:5000

## API Endpoints

- **Place an Order** (Authenticated)
  - POST `/orders`
  - Headers: `Authorization: Bearer <JWT_Token>`
  - Payload: `{"product_id": 1, "quantity": 2}`

- **Get User Orders** (Authenticated)
  - GET `/orders`
  - Headers: `Authorization: Bearer <JWT_Token>`

### Example Requests

1. **Place an Order** (as an authenticated user)

POST `http://localhost:5003/orders`

Headers:

```
Authorization: Bearer <JWT_Token>
```

Payload:

```json
{
    "product_id": 1,
    "quantity": 2
}
```

## Testing

To run unit tests for each service:

```bash
export FLASK_APP='src/app.py'
export DATABASE_URL="mysql+pymysql://username:password@hostname:3306/testdb"
export TEST='TRUE'
export USER_SERVICE_URL='http://localhost:5100' # Replace with the actual url
export PRODUCT_SERVICE_URL='http://localhost:5101' # Replace with the actual url
python -m unittest discover tests
```
