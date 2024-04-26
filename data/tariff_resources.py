from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data.tariff import Tariff
from data import db_session


def abort_if_tariff_not_found(tariff_id):
    session = db_session.create_session()
    news = session.query(Tariff).get(tariff_id)
    if not news:
        abort(404, message=f"Tariff {tariff_id} not found")


class TariffResource(Resource):
    def get(self, tariff_id):
        abort_if_tariff_not_found(tariff_id)
        session = db_session.create_session()
        tariff = session.query(Tariff).get(tariff_id)
        return jsonify({'tariff': tariff.to_dict(
            only=('name_tariff', 'quantity_gb', 'quantity_minuts', 'quantity_sms', 'coast'))})

    def delete(self, tariff_id):
        abort_if_tariff_not_found(tariff_id)
        session = db_session.create_session()
        tariff = session.query(Tariff).get(tariff_id)
        session.delete(tariff)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('name_tariff', required=True)
parser.add_argument('quantity_gb', required=True, type=int)
parser.add_argument('quantity_minuts', required=True, type=int)
parser.add_argument('quantity_sms', required=True, type=int)
parser.add_argument('coast', required=True, type=int)


class TariffListResource(Resource):
    def get(self):
        session = db_session.create_session()
        tariff = session.query(Tariff).all()
        return jsonify({'tariff': [item.to_dict(
            only=('name_tariff', 'quantity_gb', 'quantity_minuts', 'quantity_sms', 'coast')) for item in tariff]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        tariff = Tariff()
        tariff.quantity_gb = args['name_tariff']
        tariff.quantity_gb = args['quantity_gb']
        tariff.quantity_minuts = args['quantity_minuts']
        tariff.quantity_sms = args['quantity_sms']
        tariff.coast = args['coast']

        session.add(tariff)
        session.commit()
        return jsonify({'id': tariff.id})
