import os
import unittest
from typing import Optional

import requests

from src.app import app
from src.config import SQLALCHEMY_DATABASE_URI
from src.models import db
from src.service import OrderService


class TestApp(unittest.TestCase):
    service = OrderService()
    username = "test_orders@cloudaeye.com"
    password = "Admin@1234"
    access_token: Optional[str] = None
    product = {
        "name": "Test Product",
        "description": "Test product created to test order e2e",
        "price": 9.99,
        "quantity": 1000
    }

    order_id: Optional[int] = None

    @classmethod
    def setUpClass(cls):
        app.config['TEST_MODE'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        cls.app = app.test_client()
        with app.app_context():
            db.create_all()
        user_service_url = os.getenv('USER_SERVICE_URL', '')
        requests.post(f'{user_service_url}/register', json={'username': cls.username, 'password': cls.password})
        login_response = requests.post(f'{user_service_url}/login',
                                       json={'username': cls.username, 'password': cls.password})
        print(f"Login responses code : {login_response.status_code}")
        cls.access_token = login_response.json().get("access_token", "")
        with app.app_context():
            print("Clear orphan orders from prev runs (if any)")
            OrderService().delete_all_orders()

    def test_01_list_orders_endpoint_empty_items(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        response = self.app.get('/orders', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual([], response.json)

    def test_02_add_order_endpoint(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        # Add product
        product_service_url = os.getenv('PRODUCT_SERVICE_URL', '')
        product_response = requests.post(f'{product_service_url}/products', json=self.product, headers=headers)
        self.assertEqual(product_response.status_code, 201)
        added_product_id = product_response.json().get('id', None)
        self.assertIsNotNone(added_product_id)
        order_response = self.app.post('/orders', headers=headers, json={
            "product_id": added_product_id,
            "quantity": 10
        })
        self.assertEqual(order_response.status_code, 201)
        order_id = order_response.json.get("id", None)
        self.assertIsNotNone(order_id)
        requests.delete(f'{product_service_url}/products/{added_product_id}', json=self.product, headers=headers)



if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = None  # None to keep the method definition order
    unittest.TextTestRunner().run(test_loader.loadTestsFromTestCase(TestApp))
