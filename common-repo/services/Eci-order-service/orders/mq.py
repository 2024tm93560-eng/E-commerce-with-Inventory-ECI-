import os, json, pika
from datetime import datetime, timezone

RABBIT_URL       = os.getenv("RABBITMQ_URL") or os.getenv("RABBIT_URL", "amqp://eci:eci123@rabbitmq:5672/")
ORDERS_EXCHANGE  = os.getenv("ORDERS_EXCHANGE", "orders.x")
ORDERS_ROUTING   = os.getenv("ORDERS_ROUTING_KEY", "order.confirmed")


def _channel():
    params = pika.URLParameters(RABBIT_URL)
    conn = pika.BlockingConnection(params)
    ch = conn.channel()
    ch.exchange_declare(exchange=ORDERS_EXCHANGE, exchange_type="topic", durable=True)
    return conn, ch


def publish_order_confirmed(order_payload: dict):
    """
    Publishes a normalized order.confirmed event to RabbitMQ.
    Expected keys:
        to, customer.email, order.id, order.total, order.currency
    """
    # Add metadata timestamp (non-destructive)
    order_payload["event"] = "order.confirmed"
    order_payload["created_at"] = datetime.now(timezone.utc).isoformat()

    body = json.dumps(order_payload, ensure_ascii=False).encode("utf-8")

    conn, ch = _channel()
    try:
        ch.basic_publish(
            exchange=ORDERS_EXCHANGE,
            routing_key=ORDERS_ROUTING,
            body=body,
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2
            ),
        )
    finally:
        conn.close()
