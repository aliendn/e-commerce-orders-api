
# 🛒 E-Commerce Orders API (Serverless, Python, AWS Lambda)

A lightweight, serverless Order Management API built using:

- ✅ AWS Lambda + API Gateway (REST)
- 🧰 AWS Lambda Powertools for Python (logging, tracing, metrics, idempotency, feature flags)
- 📦 DynamoDB as the order database
- 🛠️ Pydantic for request validation
- 🚀 LocalStack for local AWS emulation and testing

---

## 📌 Features

- Create and fetch orders
- Type-safe payloads with validation using Pydantic
- Idempotent `POST /order` endpoint (prevents double orders)
- Feature flags controlled via AWS AppConfig
- Metrics, logs, and tracing via Powertools
- Fully local development possible with LocalStack

---

## 🧱 Architecture

```
Client → API Gateway → Lambda (APIGatewayRestResolver + Pydantic)
                                   ├── DynamoDB (Orders table)
                                   ├── AWS AppConfig (feature flags)
                                   ├── AWS CloudWatch (metrics/logs)
                                   └── AWS X-Ray (tracing)
```

---

## 🧰 Tech Stack

| Layer           | Tool / Library                                |
|-----------------|------------------------------------------------|
| API             | AWS API Gateway (REST)                        |
| Function        | AWS Lambda (Python 3.11)                      |
| Framework       | AWS Lambda Powertools                        |
| Routing         | APIGatewayRestResolver                        |
| Validation      | Pydantic                                      |
| Database        | DynamoDB                                      |
| Local Testing   | LocalStack                                    |
| IaC             | AWS SAM                                       |

---

## 📁 Project Structure

```
ecommerce-orders/
├── app.py                  # Lambda handler + routing
├── models.py               # Pydantic data models
├── requirements.txt
├── utils/
│   ├── db.py               # DynamoDB helpers
│   └── features.py         # Feature flags
├── template.yaml           # AWS SAM template
└── README.md
```

---

## 🚀 Getting Started

### 1. Install Tools

Make sure you have the following installed:

- 🐍 Python 3.11+
- 🐳 Docker (for LocalStack)
- 📦 AWS CLI
- 📦 AWS SAM CLI → https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
- 📦 LocalStack → https://docs.localstack.cloud/getting-started/installation/

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

### 2. Run Locally with LocalStack

#### Start LocalStack:

```bash
localstack start -d
```

#### Create DynamoDB Table:

```bash
awslocal dynamodb create-table   --table-name Orders   --attribute-definitions AttributeName=order_id,AttributeType=S   --key-schema AttributeName=order_id,KeyType=HASH   --billing-mode PAY_PER_REQUEST
```

#### Deploy Lambda Function (SAM + LocalStack):

```bash
sam build
AWS_ENDPOINT_URL=http://localhost:4566 sam deploy --guided   --parameter-overrides "Environment=local"
```

---

### 3. Usage

#### POST /order

Creates an order.

```bash
curl -X POST http://localhost:4566/restapis/{api_id}/local/_user_request_/order   -H "Content-Type: application/json"   -d '{"customer": "John Doe", "items": ["item1", "item2"]}'
```

#### GET /order/{order_id}

Fetch a specific order:

```bash
curl http://localhost:4566/restapis/{api_id}/local/_user_request_/order/{order_id}
```

---

## ⚙️ Environment Variables

These are used internally by Powertools:

```env
POWERTOOLS_SERVICE_NAME=orders
POWERTOOLS_METRICS_NAMESPACE=EcommerceApp
```

---

## 🧠 Developer Notes

### Powertools Modules Used:
- `Logger`: structured logging
- `Tracer`: distributed tracing via AWS X-Ray
- `Metrics`: custom CloudWatch metrics
- `Idempotency`: safely retryable functions
- `Feature Flags`: staged rollouts

### Advanced Enhancements (TODO):
- SQS integration for async processing
- Add JWT-based auth (Cognito/JWT + Lambda Authorizer)
- Pagination and filters on `GET /order`
- GitHub Actions CI/CD

---

## 📚 References

- 📖 [AWS Lambda Powertools Docs](https://docs.powertools.aws.dev/lambda/python/latest/)
- 📖 [LocalStack Docs](https://docs.localstack.cloud/)
- 📖 [SAM CLI Docs](https://docs.aws.amazon.com/serverless-application-model/)

---

## 📄 License

MIT License - feel free to fork, improve, and reuse!