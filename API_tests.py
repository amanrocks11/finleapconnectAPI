import API_builder
import API_methods
from assertpy import assert_that
import logging
import re
from urllib.parse import urlparse
from datetime import date

# for validating an Email
regex_email = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
# for validating an id is numeric
regex_id = r'^\d+$'

# Test Data
name = 'Aman'
job = 'MTS'

LOGGER = logging.getLogger(__name__)


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


# Tests for LIST USERS API

def test_list_users_response_code():
    url = API_builder.url_builder(API_builder.list_user_endpoint, '2')
    response = API_methods.list_users(url)
    assert_that(response.ok, 'HTTP Request OK').is_true()


def test_list_users_page_number():
    url = API_builder.url_builder(API_builder.list_user_endpoint, '2')
    response = API_methods.list_users(url)
    assert_that(response.json()['page']).is_equal_to(2)


def test_list_users_keys():
    expected_keys = (['page', 'per_page', 'total', 'total_pages', 'data', 'ad'])
    url = API_builder.url_builder(API_builder.list_user_endpoint, '2')
    actual_keys = list(API_methods.list_users(url).json().keys())
    assert_that(actual_keys).is_equal_to(expected_keys)


def test_list_users_data_keys():
    expected_keys = (['id', 'email', 'first_name', 'last_name', 'avatar'])
    url = API_builder.url_builder(API_builder.list_user_endpoint, '2')
    actual_keys = list(API_methods.list_users(url).json()['data'][0].keys())
    assert_that(actual_keys).is_equal_to(expected_keys)


def test_list_users_data_validation():
    url = API_builder.url_builder(API_builder.list_user_endpoint, '2')
    response = API_methods.list_users(url).json()['data']
    for (item) in response:
        assert_that(re.search(regex_id, str(item['id']))).is_not_equal_to(None)
        assert_that(re.search(regex_email, item['email'])).is_not_equal_to(None)
        assert_that(is_url(item['avatar'])).is_true()


# Tests for CREATE API

def test_create_user_response():
    url = API_builder.url_builder(API_builder.create_user_endpoint)
    response = API_methods.create_user(url, name, job)
    assert_that(response.ok, 'HTTP Request OK').is_true()


def test_create_user_response_validation():
    url = API_builder.url_builder(API_builder.create_user_endpoint)
    response = API_methods.create_user(url, name, job).json()
    assert_that(response['name']).is_equal_to(name)
    assert_that(response['job']).is_equal_to(job)


def test_create_user_created_date_check():
    url = API_builder.url_builder(API_builder.create_user_endpoint)
    response = API_methods.create_user(url, name, job).json()
    assert_that(response['createdAt']).contains(str(date.today()))
