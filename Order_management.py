from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order = db.relationship('Order', backref=db.backref('order_details', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_details', lazy=True))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.serialize() for order in orders])

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    customer_name = data.get('customer_name')
    total_amount = data.get('total_amount')
    order_details = data.get('order_details')

    new_order = Order(customer_name=customer_name, total_amount=total_amount)
    db.session.add(new_order)
    db.session.commit()

    for detail in order_details:
        product_id = detail.get('product_id')
        quantity = detail.get('quantity')
        new_order_detail = OrderDetail(order_id=new_order.id, product_id=product_id, quantity=quantity)
        db.session.add(new_order_detail)
        db.session.commit()

    return jsonify({'message': 'Order created successfully'}), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)