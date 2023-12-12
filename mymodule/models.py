class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name


class Category:
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name


class Record:
    def __init__(self, record_id, user_id, category_id, created_at, amount):
        self.record_id = record_id
        self.user_id = user_id
        self.category_id = category_id
        self.created_at = created_at
        self.amount = amount
