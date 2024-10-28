import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Order(db.Model):
    @staticmethod
    def get_table_name():
        if os.getenv('TEST_MODE', 'FALSE') == 'TRUE':
            return 'order_test'
        return 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')

    # Set __tablename__ dynamically based on the environment
    __table_args__ = {'extend_existing': True}
    __tablename__ = get_table_name()

