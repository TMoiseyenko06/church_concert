from schema import ma
from marshmallow import fields

class Person(ma.Schema):
    id = fields.Integer(required=False)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    plus_hash = fields.String(required=False)
    checked_in = fields.Boolean(required=False)

    class Meta():
        fields = ("id","first_name","last_name","email","plus_hash","checked_in")

person_schema = Person()
persons_schema = Person(many=True)


class Hash(ma.Schema):
    plus_hash = fields.String(required=True)
    test = fields.String(required=False)

    class Meta():
        fields=("plus_hash","test")

hash_schema = Hash()