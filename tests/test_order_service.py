import unittest

from src.app import app
from src.config import SQLALCHEMY_DATABASE_URI
from src.models import Order, db
from src.service import OrderService


class TestOrderService(unittest.TestCase):
    service = OrderService()
    orders = [{
        "product_id": 12,
        "quantity": 10
    }, {
        "product_id": 13,
        "quantity": 100
    }, {
        "product_id": 14,
        "quantity": 160
    }]
    user_orders: dict = {}

    @classmethod
    def setUpClass(cls):
        print("setting up")
        app.config['TEST_MODE'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        cls.app = app.test_client()
        with app.app_context():
            db.create_all()
        with app.app_context():
            print("Delete all orders")
            cls.service.delete_all_orders()

    @classmethod
    def tearDownClass(cls):
        print("tearing down")
        with app.app_context():
            for uid in cls.user_orders.keys():
                cls.service.delete_by_user(user_id=uid)
        cls.orders.clear()
        cls.user_orders.clear()

    def test_01_place_orders(self):
        with app.app_context():
            orders_1 = self.user_orders[1] if 1 in self.user_orders else []
            for order in self.orders:
                result: Order = self.service.create_order(user_id=1, product_id=order.get("product_id", -1), quantity=order.get("quantity", 0))
                self.assertIsNotNone(result.id)
                orders_1.append(order)
                self.user_orders[1] = orders_1
            self.assertEqual(len(orders_1), len(self.orders))
            orders_2 = self.user_orders[2] if 2 in self.user_orders else []
            for order in self.orders[0:2]:
                result: Order = self.service.create_order(user_id=2, product_id=order.get("product_id", -1), quantity=order.get("quantity", 0))
                self.assertIsNotNone(result.id)
                orders_2.append(order)
                self.user_orders[2] = orders_2
            self.assertEqual(len(orders_2), len(self.orders[0:2]))

    # def test_02_list_orders(self):
    #     with app.app_context():
    #         result = self.service.get_all_orders(user_id=1)
    #         self.assertEqual(len(result), len(self.user_orders[1]))

if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = None  # None to keep the method definition order
    unittest.TextTestRunner().run(test_loader.loadTestsFromTestCase(TestOrderService))
