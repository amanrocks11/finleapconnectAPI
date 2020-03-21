server = 'https://reqres.in/api'
list_user_endpoint = 'users?page='
create_user_endpoint = 'users'


def url_builder(endpoint, param=None):
    return server + '/' + endpoint + str(param)