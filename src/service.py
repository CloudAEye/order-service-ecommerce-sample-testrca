from src.models import Order, db


class OrderService:

    def create_order(self, user_id: int, product_id: int, quantity: int):
        try:
            # Create the order
            new_order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(new_order)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return new_order

    def get_all_orders(self, user_id: int):
        orders: list[Order] = Order.query.filter_by(user_id=user_id).all()
        return [{'id': order.id, 'user_id': user_id, 'product_id': order.product_id, 'quantity': order.quantity, 'status': order.status} for
                order
                in orders]

    def delete_all_orders(self):
        result = Order.query.delete()
        return result
