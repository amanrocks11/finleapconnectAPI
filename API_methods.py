import requests
import json


def list_users(api_url):
    """

    :param page_number:
    :return:
    """
    try:
        return requests.get(api_url)
    except Exception as e:
        print('API GET request failed with following error: '+str(e))


def create_user(api_url, name, job):
    try:
        data = {"name": name, "job": job}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        return requests.post(api_url, data=json.dumps(data), headers=headers)
    except Exception as e:
        print('API POST request failed with following error: '+str(e))
