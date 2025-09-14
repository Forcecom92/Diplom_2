import pytest
import requests
import urls
import helper
from data import TestDataBody

#Создание данных для уникального пользователя и дальнейшее его удаление
@pytest.fixture(scope='function')
def payload_data_new():
    payload = helper.TestMethodHelper.create_random_login_password()
    yield payload
    response = requests.post(urls.URL_BASE + urls.URL_AUTH, data=payload)
    token = response.json()["accessToken"]
    requests.delete(urls.URL_BASE + urls.URL_DELETE_USER, data=payload, headers={"Authorization": token})

#Создание данных для пользователя с его регистрацией, возвратом данных по регистрации и удалением измененного пользователя
@pytest.fixture(scope='function')
def patch_data():
    payload = helper.TestMethodHelper.create_random_login_password()
    response = requests.post(urls.URL_BASE + urls.URL_REG_USER, data=payload)
    yield response
    token = response.json()["accessToken"]
    requests.delete(urls.URL_BASE + urls.URL_DELETE_USER, data=TestDataBody.BODY_WITH_CHANGED_DATA,
                    headers={"Authorization": token})

#Создание двух пользователей для теста с последующим их удалением
#эти две последние фикстуры используются, по сути, только в негативных тестах, где необходимо изменить данные пользователя
@pytest.fixture(scope='function')
def two_default_users():
    payload_one = helper.TestMethodHelper.create_random_login_password()
    response_one = requests.post(urls.URL_BASE + urls.URL_REG_USER, data=payload_one)
    payload_two = helper.TestMethodHelper.create_random_login_password()
    response_two = requests.post(urls.URL_BASE + urls.URL_REG_USER, data=payload_two)
    token_two = response_two.json()["accessToken"]
    data = [payload_one, token_two]
    yield data
    token_one = response_one.json()["accessToken"]
    requests.delete(urls.URL_BASE + urls.URL_DELETE_USER, data=payload_one,
                    headers={"Authorization": token_one})
    requests.delete(urls.URL_BASE + urls.URL_DELETE_USER, data=payload_two,
                    headers={"Authorization": token_two})