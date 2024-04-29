from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data.users import User
from data import db_session
import datetime


def abort_if_users_not_found(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        abort(404, message=f"User {users_id} not found")


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        return jsonify({'users': users.to_dict(
            only=('id', 'name', 'phone_number', 'surname', 'money', 'hashed_password', 'created_date'))})

    def delete(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, users_id):
        abort_if_users_not_found(users_id)
        args = parser.parse_args()
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        session.expire_on_commit = False

        users.id = int(args['id'])
        users.name = args['name']
        users.phone_number = args['phone_number']
        users.surname = args['surname']
        users.money = args['money']
        users.created_date = datetime.datetime.strptime(args['created_date'], '%Y-%m-%d %H:%M:%S')
        users.hashed_password = args['hashed_password']

        session.merge(users)
        session.commit()
        return jsonify({'id': users.id})


parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('name', required=True)
parser.add_argument('phone_number', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('money', required=True, type=int)
parser.add_argument('created_date', required=True)
parser.add_argument('hashed_password', required=True)


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'name', 'phone_number', 'surname', 'money', 'created_date', 'hashed_password')) for item
            in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User()
        users.id = int(args['id'])
        users.name = args['name']
        users.phone_number = args['phone_number']
        users.surname = args['surname']
        users.money = args['money']
        users.created_date = datetime.datetime.strptime(args['created_date'], '%Y-%m-%d %H:%M:%S')
        users.hashed_password = args['hashed_password']

        session.add(users)
        session.commit()
        return jsonify({'id': users.id})
