from data import lots_resources, tariff_resources


def initialize_routes(api):
    api.add_resource(lots_resources.LotsListResource, '/api/lots')
    api.add_resource(lots_resources.LotsResource, '/api/lots/<int:lots_id>')
    api.add_resource(tariff_resources.TariffListResource, '/api/tariff')
    api.add_resource(tariff_resources.TariffResource, '/api/tariff/<int:tariff_id>')
