from flask import jsonify, request

from mymodule import app
from mymodule.models import User, Category, Record
from datetime import datetime

users = {}
categories = {}
records = {}
record_id_counter = 1


@app.route("/user/<int:user_id>", methods=['GET', 'DELETE'])
def get_delete_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify(message='User not found'), 404

    if request.method == 'GET':
        return jsonify(id=user.user_id, name=user.name)
    elif request.method == 'DELETE':
        del users[user_id]
        return jsonify(message='User deleted successfully')


@app.route("/users", methods=['GET'])
def get_users():
    return jsonify(users=[{'id': user.user_id, 'name': user.name} for user in users.values()])


@app.route("/user", methods=['POST'])
def create_user():
    data = request.get_json()
    if 'name' not in data:
        return jsonify(message='Name is required'), 400

    user_id = len(users) + 1
    new_user = User(user_id, data['name'])
    users[user_id] = new_user

    return jsonify(message='User created successfully', id=user_id)


@app.route("/category/<int:category_id>", methods=['GET', 'DELETE'])
def get_delete_category(category_id):
    category = categories.get(category_id)
    if not category:
        return jsonify(message='Category not found'), 404

    if request.method == 'GET':
        return jsonify(id=category.category_id, name=category.name)
    elif request.method == 'DELETE':
        del categories[category_id]
        return jsonify(message='Category deleted successfully')


@app.route("/categories", methods=['GET'])
def get_categories():
    return jsonify(categories=[{'id': category.category_id, 'name': category.name} for category in categories.values()])


@app.route("/category", methods=['POST'])
def create_category():
    data = request.get_json()
    if 'name' not in data:
        return jsonify(message='Name is required'), 400

    category_id = len(categories) + 1
    new_category = Category(category_id, data['name'])
    categories[category_id] = new_category

    return jsonify(message='Category created successfully', id=category_id)


@app.route("/record/<int:record_id>", methods=['GET', 'DELETE'])
def get_delete_record(record_id):
    record = records.get(record_id)
    if not record:
        return jsonify(message='Record not found'), 404

    if request.method == 'GET':
        return jsonify(id=record.record_id, user_id=record.user_id, category_id=record.category_id,
                       created_at=record.created_at, amount=record.amount)
    elif request.method == 'DELETE':
        del records[record_id]
        return jsonify(message='Record deleted successfully')


@app.route("/records", methods=['GET'])
def get_records():
    user_id = request.args.get("user_id")
    category_id = request.args.get("category_id")
    if not user_id and not category_id:
        return {"message": "Required parameters are not specified"}, 400
    filter = records
    if user_id:
        filter = {record_id: record for record_id, record in filter.items() if record.user_id == user_id}
    if category_id:
        filter = {record_id: record for record_id, record in filter.items() if record.category_id == category_id}
    return jsonify(records=[{'id': record.record_id, 'user_id': record.user_id, 'category_id': record.category_id, 'created_at': record.created_at, 'amount': record.amount} for record in filter.values()])


@app.route("/record", methods=['POST'])
def create_record():
    data = request.get_json()
    required_fields = ['user_id', 'category_id', 'amount']
    for field in required_fields:
        if field not in data:
            return jsonify(message=f'{field} is required'), 400

    global record_id_counter
    new_record = Record(record_id_counter, data['user_id'], data['category_id'], datetime.now(), data['amount'])
    records[record_id_counter] = new_record
    record_id_counter += 1

    return jsonify(message='Record created successfully', id=record_id_counter - 1)
