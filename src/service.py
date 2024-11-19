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

    def get_all_orders(self, user_id: int) -> [dict]:
        orders: list[Order] = Order.query.filter_by(user_id=user_id).all()
        print(f"Total order for the user - {user_id} : {len(orders)}")
        return [{'id': order.id, 'user_id': user_id, 'product_id': order.product_id, 'quantity': order.quantity, 'status': order.status} for
                order
                in orders]

    def delete_by_user(self, user_id):
        """
        Deletes all orders created by the given user
        :param user_id: Id of the user
        :return: Success message
        """
        orders: [Order] = Order.query.filter_by(user_id=user_id).all()
        for order in orders:
            db.session.delete(order)
            db.session.commit()
        return True


    def delete_all_orders(self):
        """
        Deletes all orders in the db
        :return:
        """
        orders: [Order] = Order.query.all()
        for order in orders:
            db.session.delete(order)
            db.session.commit()
        return True
