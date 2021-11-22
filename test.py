import datetime as dt
from marshmallow import Schema, fields, post_load, ValidationError
from pprint import pprint

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class BandMemberSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email()

user_data =  [
    {"email": "mick@stones.com", "name": "Mick"},
    {"email": "invalid", "name": "Invalid"}, # invalid email
    {"email": "keith@stones.com", "name": "Keith"},
    {"email": "charlie@stones.com"}, # missing "Name"
]

try:
    BandMemberSchema(many=True).load(user_data)
except ValidationError as err:
    pprint(err.messages)


# try:
#     result = UserSchema().load({"name": "John", "email": "foo"})
# except ValidationError as err:
#     print(err.messages) # =? {"email": ['"foo" is not a valid email address.']}
#     print(err.valid_data) # => {"name": "John"}


# user1 = User(name="Mick", email="mick@stones.com")
# user2 = User(name="Keith", email="keith@stones.com")
# users = [user1, user2]
# schema = UserSchema(many=True)
# result = schema.dump(users) # OR UserSchema().dump(users, many=True)
# pprint(result)


# user_data = {"name": "Ronnie", "email": "ronnie@stones.com"}
# schema = UserSchema()
# result = schema.load(user_data)
# print(result) # => <User(name='Ronnie')>


# user = User(name="Monty", email="monty@python.org")
# schema = UserSchema()
# result = schema.dump(user)
# pprint(result)


# user_data = {
#     "created_at": "2014-08-11T05:25:03.869245",
#     "email": "ken@yahoo.com",
#     "name": "Ken",
# }
# schema = UserSchema()
# result = schema.load(user_data)
# pprint(result)
