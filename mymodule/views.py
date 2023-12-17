from mymodule import app, db
from flask import request, jsonify
from marshmallow import *
from . import schemas
from .models import UserModel
from .models import BankAccountModel
from .models import CategoryModel
from .models import RecordModel
from . import models


def add(data):
    db.session.add(data)
    db.session.commit()


def update():
    db.session.commit()


def delete(data):
    db.session.delete(data)
    db.session.commit()


@app.post('/user')
def create_user():
    user_data = request.get_json()
    try:
        schemas.UserSchema().load({"name": user_data["name"]})
        if db.session.query(UserModel).filter(UserModel.name == user_data["name"]).first() is None:
            user = UserModel(user_data["name"])
            add(user)
            schemas.BankAccountSchema().load({"user_id": user.id, "money": user_data["money"]})
            account = BankAccountModel(user.id, user_data["money"])
            add(account)
            return jsonify({"id": user.id, "name": user.name, "money": account.money})
        else:
            return "UserExist, 404"
    except ValidationError as error:
        return error.messages


@app.get('/user/account')
def get_account():
    user_id = request.args.get('userID')
    try:
        account = db.session.query(BankAccountModel).filter(BankAccountModel.user_id == user_id).first()
        return jsonify({"user_id": account.user_id, "money": account.money})
    except AttributeError:
        return "AttributeError, 404"


@app.get('/user')
def get_user():
    user_id = request.args.get('userID')
    try:
        user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
        return jsonify({"id": user.id, "name": user.name})
    except AttributeError:
        return "AttributeError, 404"


@app.delete('/user')
def delete_user():
    user_id = request.args.get('userID')
    try:
        user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
        deleted_user = {"id": user.id, "name": user.name}
        delete(user)
        return jsonify(deleted_user)
    except AttributeError:
        return "AttributeError, 404"


@app.get('/users')
def get_users():
    users = [{"id": user.id, "name": user.name} for user in db.session.query(UserModel).all()]
    return jsonify(users)


@app.post('/category')
def create_category():
    category_data = request.get_json()
    try:
        schemas.CategorySchema().load({"name": category_data["name"]})
        if db.session.query(CategoryModel).filter(CategoryModel.name == category_data["name"]).first() is None:
            category = CategoryModel(category_data["name"])
            add(category)
            return jsonify({"id": category.id, "name": category.name})
        else:
            return "CategoryExist, 404"
    except ValidationError as error:
        return error.messages


@app.get('/category')
def get_category():
    category_id = request.args.get('categoryID')
    try:
        schemas.CategorySchema().load({"id": category_id, "name": "instance"})
        try:
            category = db.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
            return jsonify({"id": category.id, "name": category.name})
        except AttributeError:
            return "AttributeError, 404"
    except ValidationError as error:
        return error.messages


@app.get('/categories')
def get_categories():
    categories = [{"id": category.id, "name": category.name} for category in db.session.query(CategoryModel).all()]
    return jsonify(categories)


@app.delete('/category')
def delete_category():
    category_id = request.args.get('categoryID')
    try:
        category = db.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        deleted_category = {"id": category.id, "name": category.name}
        delete(category)
        return jsonify(deleted_category)
    except AttributeError:
        return "AttributeError, 404"


@app.post('/record')
def create_record():
    user_id = request.args.get('userID')
    category_id = request.args.get('categoryID')
    amount_of_expenditure = request.args.get('amount')
    try:
        schemas.RecordSchema().load(
            {"user_id": user_id, "category_id": category_id, "amount_of_expenditure": amount_of_expenditure})
        if db.session.get(models.UserModel, user_id) is not None and db.session.get(models.CategoryModel,
                                                                                    category_id) is not None:
            account = db.session.query(models.BankAccountModel).filter(models.BankAccountModel.user_id == user_id).first()
            if account is not None and account.money - float(amount_of_expenditure) > 0:
                account.money = account.money - float(amount_of_expenditure)
                update()
                record = models.RecordModel(user_id, category_id, amount_of_expenditure)
                add(record)
                return jsonify(
                    {"id": record.id, "user_id": record.user_id, "category_id": record.category_id, "time": record.time,
                     "amount_of_expenditure": record.amount_of_expenditure})
            else:
                return "user account isn't exist or insufficient funds"
        else:
            return "user or category isn't exist"
    except ValidationError as error:
        return error.messages


@app.get('/record')
def get_record():
    user_id = request.args.get('userID')
    category_id = request.args.get('categoryID')
    try:
        schemas.RecordSchema().load({"user_id": user_id, "category_id": category_id, "amount_of_expenditure": 1.0})
        try:
            record = db.session.query(RecordModel).filter(RecordModel.user_id == user_id,
                                                          RecordModel.category_id == category_id).first()
            return jsonify(
                {"id": record.id, "user_id": record.user_id, "category_id": record.category_id, "time": record.time,
                 "amount_of_expenditure": record.amount_of_expenditure})
        except AttributeError:
            return "AttributeError, 404"
    except ValidationError as error:
        return error.messages


@app.delete('/record')
def delete_record():
    record_id = request.args.get('recordID')
    if record_id.isdigit():
        try:
            record = db.session.query(RecordModel).filter(RecordModel.id == record_id).first()
            deleted_record = {"id": record.id, "user_id": record.user_id, "category_id": record.category_id,
                              "time": record.time, "amount_of_expenditure": record.amount_of_expenditure}
            delete(record)
            return jsonify(deleted_record)
        except AttributeError:
            return "AttributeError, 404"
    else:
        return "sqlalchemy.exc.DataError"
