from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data.paket_users import Paket_Users
from data import db_session
import datetime


def abort_if_paket_users_not_found(paket_users_id):
    session = db_session.create_session()
    paket_users = session.query(Paket_Users).get(paket_users_id)
    if not paket_users:
        abort(404, message=f"Paket_Users {paket_users_id} not found")


class PaketUsersResource(Resource):
    def get(self, paket_users_id):
        abort_if_paket_users_not_found(paket_users_id)
        session = db_session.create_session()
        paket_users = session.query(Paket_Users).get(paket_users_id)
        return jsonify({'paket_users': paket_users.to_dict(
            only=(
                'id', 'tariff_connect', 'quantity_gb', 'quantity_minuts', 'quantity_sms', 'date_renewal_tariff',
                'user_id',
                'tariff_id'))})

    def delete(self, paket_users_id):
        abort_if_paket_users_not_found(paket_users_id)
        session = db_session.create_session()
        paket_users = session.query(Paket_Users).get(paket_users_id)
        session.delete(paket_users)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, paket_users_id):
        abort_if_paket_users_not_found(paket_users_id)
        args = parser.parse_args()
        session = db_session.create_session()
        paket_users = session.query(Paket_Users).get(paket_users_id)
        session.expire_on_commit = False

        paket_users.id = int(args['id'])
        paket_users.tariff_connect = args['tariff_connect']
        paket_users.quantity_gb = args['quantity_gb']
        paket_users.quantity_minuts = args['quantity_minuts']
        paket_users.quantity_sms = args['quantity_sms']
        paket_users.date_renewal_tariff = datetime.datetime.strptime(args['date_renewal_tariff'], '%Y-%m-%d %H:%M:%S')
        paket_users.user_id = args['user_id']
        paket_users.tariff_id = args['tariff_id']

        session.merge(paket_users)
        session.commit()
        return jsonify({'id': paket_users.id})


parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('tariff_connect', required=True, type=int)
parser.add_argument('quantity_gb', required=True, type=float)
parser.add_argument('quantity_minuts', required=True, type=int)
parser.add_argument('quantity_sms', required=True, type=int)
parser.add_argument('date_renewal_tariff', required=True)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('tariff_id', required=True, type=int)


class PaketUsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        paket_users = session.query(Paket_Users).all()
        return jsonify({'paket_users': [item.to_dict(
            only=(
                'id', 'tariff_connect', 'quantity_gb', 'quantity_minuts', 'quantity_sms', 'date_renewal_tariff',
                'user_id',
                'tariff_id')) for item
            in paket_users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        paket_users = Paket_Users()
        paket_users.id = int(args['id'])
        paket_users.tariff_connect = args['tariff_connect']
        paket_users.quantity_gb = args['quantity_gb']
        paket_users.quantity_minuts = args['quantity_minuts']
        paket_users.quantity_sms = args['quantity_sms']
        paket_users.date_renewal_tariff = datetime.datetime.strptime(args['date_renewal_tariff'], '%Y-%m-%d %H:%M:%S')
        paket_users.user_id = args['user_id']
        paket_users.tariff_id = args['tariff_id']

        session.add(paket_users)
        session.commit()
        return jsonify({'id': paket_users.id})
