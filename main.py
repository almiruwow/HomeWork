from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from data import users, offers, orders
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, default=datetime.utcnow)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))



@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        user_data = []
        for user in User.query.all():
            user_data.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age' : user.age,
                'email': user.email,
                'role': user.role,
                'phone':  user.phone
            })

        return jsonify(user_data)

    elif request.method == 'POST':
        json_data = request.get_json()
        with db.session.begin():
            db.session.add(User(
                first_name=json_data.get('first_name'),
                last_name=json_data.get('last_name'),
                age=json_data.get('age'),
                email=json_data.get('email'),
                role=json_data.get('role'),
                phone=json_data.get('phone')
            ))

        return f'Пользователь успешно добавлен'


@app.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def users_id(uid):
    if request.method == 'GET':
        data = {
            'id': User.query.get(uid).id,
            'first_name': User.query.get(uid).first_name,
            'last_name': User.query.get(uid).last_name,
            'age': User.query.get(uid).age,
            'email': User.query.get(uid).email,
            'role': User.query.get(uid).role,
            'phone': User.query.get(uid).phone
        }

        return jsonify(data)

    elif request.method == 'PUT':
        data_update = User.query.get(uid)
        data_json = request.get_json()
        data_update.first_name = data_json.get('first_name')
        data_update.last_name = data_json.get('last_name')
        data_update.age = data_json.get('age')
        data_update.email = data_json.get('email')
        data_update.role = data_json.get('role')
        data_update.phone = data_json.get('phone')


        db.session.add(data_update)
        db.session.commit()

        return f'Пользователь успешно обновлен'

    elif request.method == 'DELETE':
        data_delete = User.query.get(uid)

        db.session.delete(data_delete)
        db.session.commit()

        return f'Пользователь успешно удален'


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        orders_data = []
        for order in Order.query.all():
            orders_data.append({
                'id': order.id,
                'name': order.name,
                'description': order.description,
                'start_date': order.start_date,
                'end_date': order.end_date,
                'address': order.address,
                'price': order.price,
                'customer_id': order.customer_id,
                'executor_id': order.executor_id
            })

        return jsonify(orders_data)

    elif request.method == 'POST':
        json_data = request.get_json()

        with db.session.begin():
            db.session.add(Order(
                name=json_data.get('name'),
                description=json_data.get('description'),
                start_date=datetime.strptime(json_data.get('start_date'), '%m/%d/%Y'),
                end_date=datetime.strptime(json_data.get('end_date'), '%m/%d/%Y'),
                address=json_data.get('address'),
                price=json_data.get('price'),
                customer_id=json_data.get('customer_id'),
                executor_id=json_data.get('executor_id')
            ))

        return 'Заказ добавлен'


@app.route('/orders/<int:oid>', methods=['GET', 'PUT', 'DELETE'])
def orders_id(oid):
    if request.method == 'GET':
        data = {
            'id': Order.query.get(oid).id,
            'name': Order.query.get(oid).name,
            'description': Order.query.get(oid).description,
            'start_date': Order.query.get(oid).start_date,
            'end_date': Order.query.get(oid).end_date,
            'address': Order.query.get(oid).address,
            'price': Order.query.get(oid).price,
            'customer_id': Order.query.get(oid).customer_id,
            'executor_id': Order.query.get(oid).executor_id
        }
        return jsonify(data)

    elif request.method == 'PUT':
        data_update = Order.query.get(oid)
        data_json = request.get_json()
        data_update.name = data_json.get('name')
        data_update.description = data_json.get('description')
        data_update.start_date = datetime.strptime(data_json.get('start_date'), '%m/%d/%Y')
        data_update.end_date = datetime.strptime(data_json.get('end_date'), '%m/%d/%Y')
        data_update.address = data_json.get('address')
        data_update.price = data_json.get('price')
        data_update.customer_id = data_json.get('customer_id')
        data_update.executor_id = data_json.get('executor_id')

        db.session.add(data_update)
        db.session.commit()

        return f'Заказ успешно обновлен'

    elif request.method == 'DELETE':
        data_delete = Order.query.get(oid)
        db.session.delete(data_delete)
        db.session.commit()

        return f'Заказ успешно удален'


@app.route('/offers', methods=['GET', 'POST'])
def offers():
    if request.method == 'GET':
        offer_data = []
        for offer in Offer.query.all():
            ex_id = User.query.get(offer.executor_id)
            or_id = Order.query.get(offer.order_id)
            offer_data.append({
                'id': offer.id,
                'order_id': or_id.name,
                'executor_id': ex_id.first_name
            })

        return jsonify(offer_data)

    elif request.method == 'POST':
        data_json = request.get_json()
        with db.session.begin():
            db.session.add(Offer(
                order_id=data_json.get('order_id'),
                executor_id=data_json.get('executor_id')
            ))

        return 'Оффер успешно добавлен'


@app.route('/offers/<int:oid>', methods=['GET', 'PUT', 'DELETE'])
def offer_id(oid):
    if request.method == 'GET':
        offer_return = Offer.query.get(oid)
        data = {
            'id': offer_return.id,
            'order_id': Order.query.get(offer_return.order_id).name,
            'executor_id': User.query.get(offer_return.executor_id).first_name
        }
        return jsonify(data)

    elif request.method == 'PUT':
        data_update = Offer.query.get(oid)
        data_json = request.get_json()
        data_update.order_id = data_json.get('order_id')
        data_update.executor_id = data_json.get('executor_id')

        db.session.add(data_update)
        db.session.commit()

        return 'Оффер успешно обновлен'

    elif request.method == 'DELETE':
        data_delete = Offer.query.get(oid)
        db.session.delete(data_delete)
        db.session.commit()

        return 'Оффер успешно удален'


if __name__ == '__main__':
    app.run(debug=True)

