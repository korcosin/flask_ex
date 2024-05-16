from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import urllib.parse
import os

# sudo apt install python3-pip
# pip3 install flask sqlalchemy psycopg2, Flask-SQLAlchemy

HOST = os.environ['POSTGRES_HOST']
PORT = 5432
DATABASE_NAME = os.environ['POSTGRES_DB']
USER = os.environ['POSTGRES_USER']
PASSWORD = urllib.parse.quote_plus(os.environ['POSTGRES_PASSWORD'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}'
db = SQLAlchemy(app)

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    name = db.Column(db.String())
    role_id = db.Column(db.Integer)

@app.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    admins = (
        Admin.query.order_by(desc(Admin.id))
        .limit(limit).offset((page - 1) * limit)
        .all()
    )
    admin_list = [{
        'id': admin.id, 
        'email': admin.email, 
        'name': admin.name, 
        'role_id': admin.role_id
    } for admin in admins]

    return jsonify(admin_list), 200

@app.route('/<int:admin_id>', methods=['GET'])
def show(admin_id):
    admin = Admin.query.get(admin_id)
    return jsonify({
        'id': admin.id, 
        'email': admin.email, 
        'name': admin.name, 
        'role_id': admin.role_id
    }), 200

@app.route('/', methods=['POST'])
def create():
    data = request.get_json()
    email = data['name']
    name = data['name']
    role_id = data['role_id']
    
    admin = Admin(email=email, name=name, age=role_id)
    db.session.add(admin)
    db.session.commit()
    
    return jsonify({'message': 'Insert!!'}), 201

@app.route('/<int:admin_id>', methods=['PUT'])
def update(admin_id):
    admin = Admin.query.get(admin_id)
    data = request.get_json()
    admin.email = data['email']
    admin.name = data['name']
    admin.role_id = data['role_id']
    db.session.commit()
    
    return jsonify({'message': 'Update!!'}), 200

@app.route('/<int:admin_id>', methods=['DELETE'])
def delete(admin_id):
    admin = Admin.query.get(admin_id)
    db.session.delete(admin)
    db.session.commit()
    
    return jsonify({'message': 'Deleted!!'}), 200

# python3 app.py
if __name__ == '__main__':
    app.run(debug=True)
