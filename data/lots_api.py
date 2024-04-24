import flask

from data import db_session
from data.lots import Lots

blueprint = flask.Blueprint(
    'lots_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/lots')
def get_lots():
    return "Обработчик в news_api"
