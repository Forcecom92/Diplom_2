import allure
import requests
import urls
from data import TestDataBody

class TestCreateUser:
    @allure.title('Создание уникального пользователя')
    @allure.description ('Проверям успешное создание пользователя, статус 200 и соответствие тела ответа согласно документации API')
    def test_create_user(self, payload_data_new):
        response = requests.post(urls.URL_BASE + urls.URL_REG_USER, data = payload_data_new)
        assert response.status_code == 200 and TestDataBody.body_keys in TestDataBody.BODY_OK_REGISTRATION_AUTH

    @allure.title('Создание пользователя, который уже зарегистрирован')
    @allure.description('Проверям, что повторное создание существующего пользователя невозможно, код ответа 403 и текст, согласно документации API')
    def test_create_reg_user(self, payload_data_new):
        requests.post(urls.URL_BASE + urls.URL_REG_USER, data=payload_data_new)
        response = requests.post(urls.URL_BASE + urls.URL_REG_USER, data=payload_data_new)
        assert response.status_code == 403 and response.json() == TestDataBody.user_same_name_403_body

    @allure.title('Создание пользователя без заполнениня одного из обязательных полей')
    @allure.description('Проверям, что создание пользователя без заполнения email невозможно и сообщение, согласно документации API')
    def test_empty_email(self):
        response = requests.post(urls.URL_BASE + urls.URL_REG_USER, data=TestDataBody.BODY_WITHOUT_LOGIN)
        assert response.status_code == 403 and response.json() == TestDataBody.user_without_login_403_body
