from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data.lots import Lots
from data import db_session
import datetime


def abort_if_lots_not_found(lots_id):
    session = db_session.create_session()
    news = session.query(Lots).get(lots_id)
    if not news:
        abort(404, message=f"Lots {lots_id} not found")


class LotsResource(Resource):
    def get(self, lots_id):
        abort_if_lots_not_found(lots_id)
        session = db_session.create_session()
        lots = session.query(Lots).get(lots_id)
        return jsonify({'lots': lots.to_dict(
            only=('id', 'quantity', 'price', 'user_id'))})

    def delete(self, lots_id):
        abort_if_lots_not_found(lots_id)
        session = db_session.create_session()
        lots = session.query(Lots).get(lots_id)
        session.delete(lots)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, lots_id):
        abort_if_lots_not_found(lots_id)
        args = parser.parse_args()
        session = db_session.create_session()
        lots = session.query(Lots).get(lots_id)
        session.expire_on_commit = False

        lots.id = int(args['id'])
        lots.title = args['quantity']
        lots.content = args['price']
        lots.created_date = datetime.datetime.strptime(args['created_date'], '%Y-%m-%d %H:%M:%S')
        lots.user_id = args['user_id']

        session.merge(lots)
        session.commit()
        return jsonify({'id': lots.id})


parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('quantity', required=True, type=int)
parser.add_argument('price', required=True, type=int)
parser.add_argument('created_date', required=True)
parser.add_argument('user_id', required=True, type=int)


class LotsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        lots = session.query(Lots).all()
        return jsonify({'lots': [item.to_dict(
            only=('id', 'quantity', 'price', 'created_date', 'user_id')) for item in lots]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        lots = Lots()
        lots.id = int(args['id'])
        lots.title = args['quantity']
        lots.content = args['price']
        lots.created_date = datetime.datetime.strptime(args['created_date'], '%Y-%m-%d %H:%M:%S')
        lots.user_id = args['user_id']

        session.add(lots)
        session.commit()
        return jsonify({'id': lots.id})
