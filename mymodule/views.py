from mymodule import app, db
from flask import request, jsonify, abort
from marshmallow import *
from . import marshmallow
from .models import UserModel
from .models import IncomeAccountingModel
from .models import CategoryModel
from .models import RecordModel
from . import models
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from passlib.hash import pbkdf2_sha256

jwt = JWTManager(app)
with app.app_context():
    db.create_all()
    db.session.commit()


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
   return (
       jsonify({"message": "The token has expired.", "error": "token_expired"}),
       401,
   )

@jwt.invalid_token_loader
def invalid_token_callback(error):
   return (
       jsonify(
           {"message": "Signature verification failed.", "error": "invalid_token"}
       ),
       401,
   )

@jwt.unauthorized_loader
def missing_token_callback(error):
   return (
       jsonify(
           {
               "description": "Request does not contain an access token.",
               "error": "authorization_required",
           }
       ),
       401,
   )

def add(data):
    db.session.add(data)
    db.session.commit()


def update():
    db.session.commit()


def delete(data):
    db.session.delete(data)
    db.session.commit()

@app.post('/user')
def registration_user():
    user_data = request.get_json()

    try:
        user_schema = marshmallow.UserSchema()
        user_schema.load({"name": user_data["name"], "password": user_data["password"]})

        existing_user = db.session.query(UserModel).filter(UserModel.name == user_data["name"]).first()
        if existing_user is None:
            user = UserModel(user_data["name"], password=pbkdf2_sha256.hash(user_data["password"]))
            add(user)

            income_schema = marshmallow.IncomeAccountingSchema()
            income_schema.load({"user_id": user.id, "money": user_data["money"]})

            account = IncomeAccountingModel(user.id, user_data["money"])
            add(account)

            return jsonify({"id": user.id, "name": user.name, "money": account.money})
        else:
            return jsonify({"error": "User already exists"}), 404

    except ValidationError as error:
        return jsonify({"error": error.messages}), 400


@app.post('/login-user')
def user_authorization():
    user_data = request.get_json()
    try:
        user_schema = marshmallow.UserSchema()
        user_schema.load({"name": user_data["name"], "password": user_data["password"]})

        user = db.session.query(models.UserModel).filter_by(name=user_data["name"]).first()

        access_token = create_access_token(identity=user.id)
        if not user:
            abort(404, description="user not found")

        if user.id != user_data["id"] or user.name != user_data["name"]:
            abort(401, description="invalid user ID or username")

        if not pbkdf2_sha256.verify(user_data["password"], user.password):
            abort(401, description="invalid password")

        return jsonify({"message": "Authorization successful", "token": access_token, "user_id": user.id}), 200

    except ValidationError as error:
        return jsonify({"error": error.messages}), 400
@app.get('/user/account')
@jwt_required()
def get_account():
    user_id = get_jwt_identity()

    try:
        account = db.session.query(IncomeAccountingModel).filter(IncomeAccountingModel.user_id == user_id).first()
        return jsonify({"user_id": account.user_id, "money": account.money})
    except AttributeError:
        return jsonify({"error": "AttributeError"}), 404


@app.get('/user')
@jwt_required()
def get_user():
    user_id = get_jwt_identity()

    try:
        user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
        return jsonify({"id": user.id, "name": user.name})
    except AttributeError:
        return jsonify({"error": "AttributeError"}), 404


@app.delete('/user')
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()

    try:
        user = db.session.query(UserModel).filter(UserModel.id == user_id).first()
        deleted_user = {"id": user.id, "name": user.name}
        delete(user)
        return jsonify(deleted_user)
    except AttributeError:
        return jsonify({"error": "AttributeError"}), 404

@app.get('/users')
@jwt_required()
def get_users():
    users = [{"id": user.id, "name": user.name} for user in db.session.query(UserModel).all()]
    return jsonify(users)

@app.post('/category')
@jwt_required()
def create_category():
    category_data = request.get_json()

    try:
        category_schema = marshmallow.CategorySchema()
        category_schema.load({"name": category_data["name"]})

        existing_category = db.session.query(CategoryModel).filter(CategoryModel.name == category_data["name"]).first()
        if existing_category is None:
            category = CategoryModel(category_data["name"])
            add(category)
            return jsonify({"id": category.id, "name": category.name})
        else:
            return jsonify({"error": "Category already exists"}), 404

    except ValidationError as error:
        return jsonify({"error": error.messages}), 400


@app.get('/category')
@jwt_required()
def get_category():
    category_id = request.args.get('categoryID')

    try:
        category_schema = marshmallow.CategorySchema()
        category_schema.load({"id": category_id, "name": "instance"})

        try:
            category = db.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
            return jsonify({"id": category.id, "name": category.name})
        except AttributeError:
            return jsonify({"error": "AttributeError"}), 404

    except ValidationError as error:
        return jsonify({"error": error.messages}), 400


@app.get('/categories')
@jwt_required()
def get_categories():
    categories = [{"id": category.id, "name": category.name} for category in db.session.query(CategoryModel).all()]
    return jsonify(categories)

@app.delete('/category')
@jwt_required()
def delete_category():
    category_id = request.args.get('categoryID')

    try:
        category = db.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        deleted_category = {"id": category.id, "name": category.name}
        delete(category)
        return jsonify(deleted_category)
    except AttributeError:
        return jsonify({"error": "AttributeError"}), 404


@app.post('/record')
@jwt_required()
def create_record():
    user_id = get_jwt_identity()
    category_id = request.args.get('categoryID')
    amount_of_expenditure = request.args.get('amount')

    try:
        record_schema = marshmallow.RecordSchema()
        record_schema.load(
            {"user_id": user_id, "category_id": category_id, "amount_of_expenditure": amount_of_expenditure})

        user_exists = db.session.query(models.UserModel).get(user_id)
        category_exists = db.session.query(models.CategoryModel).get(category_id)

        if user_exists is not None and category_exists is not None:
            account = db.session.query(models.IncomeAccountingModel).filter(
                models.IncomeAccountingModel.user_id == user_id).first()

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
        return jsonify({"error": error.messages}), 400


@app.get('/record')
@jwt_required()
def get_record():
    user_id = get_jwt_identity()
    category_id = request.args.get('categoryID')

    try:
        record_schema = marshmallow.RecordSchema()
        record_schema.load({"user_id": user_id, "category_id": category_id, "amount_of_expenditure": 1.0})

        try:
            record = db.session.query(RecordModel).filter(RecordModel.user_id == user_id,
                                                          RecordModel.category_id == category_id).first()
            return jsonify(
                {"id": record.id, "user_id": record.user_id, "category_id": record.category_id, "time": record.time,
                 "amount_of_expenditure": record.amount_of_expenditure})
        except AttributeError:
            return jsonify({"error": "AttributeError"}), 404

    except ValidationError as error:
        return jsonify({"error": error.messages}), 400


@app.delete('/record')
@jwt_required()
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
            return jsonify({"error": "AttributeError"}), 404
    else:
        return "sqlalchemy.exc.DataError"
