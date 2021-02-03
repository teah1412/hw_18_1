import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))

# You User model should have the following fields:
#
#     id (integer)
#     name (string)
#     email (string)
#     secret_number (integer)
#
# The secret_number field will hold the secret number that user has to guess.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    secret_number = db.Column(db.Integer, unique=False)