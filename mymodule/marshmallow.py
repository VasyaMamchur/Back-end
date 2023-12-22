from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    password = fields.String(required=True)


class IncomeAccountingSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    money = fields.Float(required=True)


class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)


class RecordSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    time = fields.Str(dump_only=True)
    amount_of_expenditure = fields.Float(required=True)