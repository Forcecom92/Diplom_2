import allure
import requests
import urls
from data import TestDataBody

class TestLoginUser:
    @allure.title('Успешная авторизация зарегистрированного пользователя')
    @allure.description ('Проверям, что зарегистрированный пользователь может авторизоваться')
    def test_auth_user(self, payload_data_new):
        requests.post(urls.URL_BASE + urls.URL_REG_USER, data = payload_data_new)
        response = requests.post(urls.URL_BASE + urls.URL_AUTH, data = payload_data_new)
        assert response.status_code == 200 and TestDataBody.body_keys in TestDataBody.BODY_OK_REGISTRATION_AUTH

    @allure.title('Неуспешная авторизация с отсутствующим обязательным полем')
    @allure.description('Проверям, что без заполнения поля email невозможно авторизоваться')
    def test_create_reg_user(self):
        response = requests.post(urls.URL_BASE + urls.URL_AUTH, data=TestDataBody.BODY_WITHOUT_LOGIN)
        assert response.status_code == 401 and response.json() == TestDataBody.user_auth_no_email_401_body

