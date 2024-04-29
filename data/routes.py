from data import lots_resources, tariff_resources, pakets_resourses, user_resoures


def initialize_routes(api):
    api.add_resource(lots_resources.LotsListResource, '/api/lots')
    api.add_resource(lots_resources.LotsResource, '/api/lots/<int:lots_id>')
    api.add_resource(tariff_resources.TariffListResource, '/api/tariff')
    api.add_resource(tariff_resources.TariffResource, '/api/tariff/<int:tariff_id>')
    api.add_resource(pakets_resourses.PaketUsersListResource, '/api/paket_users')
    api.add_resource(pakets_resourses.PaketUsersResource, '/api/paket_users/<int:paket_users_id>')
    api.add_resource(user_resoures.UsersListResource, '/api/users')
    api.add_resource(user_resoures.UsersResource, '/api/users/<int:users_id>')
