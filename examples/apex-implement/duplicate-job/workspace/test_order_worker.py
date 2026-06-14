import unittest

from order_worker import Order, OrderStore, OrderWorker, PaymentGateway


class OrderWorkerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = OrderStore()
        self.store.add(Order("order-1", 2500))
        self.gateway = PaymentGateway()
        self.worker = OrderWorker(self.store, self.gateway)

    def test_processes_an_order_once_sequentially(self) -> None:
        self.assertTrue(self.worker.process("order-1"))
        self.assertFalse(self.worker.process("order-1"))
        self.assertEqual(self.gateway.charges, [("order-1", 2500)])
        self.assertTrue(self.store.is_processed("order-1"))

    def test_unknown_order_is_not_processed(self) -> None:
        self.assertFalse(self.worker.process("missing"))
        self.assertEqual(self.gateway.charges, [])


if __name__ == "__main__":
    unittest.main()
