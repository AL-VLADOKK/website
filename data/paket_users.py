import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Paket_Users(SqlAlchemyBase):
    __tablename__ = 'paket_users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tariff_connect = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    quantity_gb = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    quantity_minuts = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    quantity_sms = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    date_renewal_tariff = sqlalchemy.Column(sqlalchemy.DateTime,
                                            default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("user.id"))
    user = orm.relationship('User', back_populates='paket_users')
    tariff_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("tariff.id"))
    tariff = orm.relationship('Tariff', back_populates='paket_users')
