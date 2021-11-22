from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound
from marshmallow import Schema, fields, ValidationError, pre_load

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/salesdb' 
db = SQLAlchemy(app)


class Authors (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    specialisation = db.Column(db.String(50))
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, specialisation):
        self.name = name
        self.specialisation = specialisation

    def __repr__(self):
        return '<Author %d>' % self.id


db.create_all()


class AuthorSchema(Schema):
    class Meta:
        model = Authors
        sqla_session = db.session
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    specialisation = fields.Str(required=True)

    
@app.route('/authors', methods=['GET'])
def index():
    get_authors = Authors.query.all()
    author_schema = AuthorSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors": authors}), 200)


@app.route('/authors', methods = ['POST'])
def create_author():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    # Validate and deserialize input
    author_schema = AuthorSchema()
    try:
        data = author_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    name, specialisation = data["name"], data["specialisation"]
    author = Authors.query.filter_by(name=name, specialisation=specialisation).first()
    if author is None:
        author = Authors(name=name, specialisation=specialisation)
        result = author_schema.dump(author.create())
        status_code = 201
    else:
        result = author_schema.dump(author)
        status_code = 200
    return make_response(jsonify({"author": result}), status_code)


@app.route('/authors/<int:id>', methods=['GET'])
def get_author_by_id(id):   
    try:
        get_author = Authors.query.get(id)
    except NoResultFound:
        return {"message": "Author could not found."}, 400
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return make_response(jsonify({"author": author}))


@app.route('/authors/<id>', methods=['PUT'])
def update_author_by_id(id):
    data = request.get_json()
    get_author = Authors.query.get(id)
    if data.get('specialisation'):
        get_author.specialisation = data['specialisation']
    if data.get('name'):
        get_author.name = data['name']
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema(only=['id', 'name', 'specialisation'])
    try:
        author = author_schema.dump(get_author)
    except ValidationError as err:
        return err.messages, 422
    return make_response(jsonify({"author": author}))


@app.route('/authors/<id>', methods=['DELETE'])
def delete_author_by_id(id):
    get_author = Authors.query.get(id)
    db.session.delete(get_author)
    db.session.commit()
    return make_response("",204)


if __name__ == "__main__":
    app.run(debug=True)