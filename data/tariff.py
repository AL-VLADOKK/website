import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from data.paket_users import Paket_Users


class Tariff(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tariff'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    quantity_gb = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    quantity_minuts = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    quantity_sms = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    coast = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    paket_users = orm.relationship('Paket_Users', back_populates='tariff')
