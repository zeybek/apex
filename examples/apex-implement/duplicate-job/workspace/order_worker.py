"""Small order-processing example with an intentional concurrency defect."""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock


@dataclass
class Order:
    order_id: str
    amount_cents: int
    processed: bool = False


class OrderStore:
    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def add(self, order: Order) -> None:
        self._orders[order.order_id] = order

    def get_unprocessed(self, order_id: str) -> Order | None:
        order = self._orders.get(order_id)
        if order is None or order.processed:
            return None
        return order

    def mark_processed(self, order_id: str) -> None:
        self._orders[order_id].processed = True

    def is_processed(self, order_id: str) -> bool:
        return self._orders[order_id].processed


class PaymentGateway:
    def __init__(self) -> None:
        self._lock = Lock()
        self.charges: list[tuple[str, int]] = []

    def charge(self, order_id: str, amount_cents: int) -> None:
        with self._lock:
            self.charges.append((order_id, amount_cents))


class OrderWorker:
    def __init__(self, store: OrderStore, gateway: PaymentGateway) -> None:
        self.store = store
        self.gateway = gateway

    def process(self, order_id: str) -> bool:
        order = self.store.get_unprocessed(order_id)
        if order is None:
            return False
        self.gateway.charge(order.order_id, order.amount_cents)
        self.store.mark_processed(order.order_id)
        return True
