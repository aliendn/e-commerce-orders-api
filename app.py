import json
import uuid
from typing import Dict

from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.utilities.idempotency import idempotent, IdempotencyConfig
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext

from utils.db import save_order, get_order
from utils.features import feature_flags
from .models import OrderRequest


logger = Logger()
tracer = Tracer()
metrics = Metrics(namespace="EcommerceApp")

app = APIGatewayRestResolver()
idempotency_config = IdempotencyConfig(event_key_jmespath="body.order_id")


@app.post("/order")
@idempotent(config=idempotency_config)
def create_order():
    try:
        body = app.current_event.json_body
        order = OrderRequest(**body)
    except Exception as e:
        raise BadRequestError("Invalid order payload")

    order_id = order.order_id or str(uuid.uuid4())

    if feature_flags.evaluate(name="validate_items", context={"items": order.items}):
        logger.info("Feature flag: Item validation enabled")

    save_order(order_id, order.customer, order.items)
    metrics.add_metric(name="OrdersCreated", unit=MetricUnit.Count, value=1)

    return {"message": "Order created", "order_id": order_id}


@app.get("/order/<order_id>")
def get_order_handler(order_id: str):
    result = get_order(order_id)
    if not result:
        return {"message": "Order not found"}, 404
    return result


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: Dict, context: LambdaContext) -> Dict:
    return app.resolve(event, context)