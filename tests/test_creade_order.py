import requests
import pytest
import allure
from data import CreateCourier
from url import Url

class TestCreadeOrder:

    @allure.title('Создание заказа с разными цветами')
    @allure.description('Тест создание заказа черным , белым, c двумя цветами')
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"] , ["BLACK", "GREY"], []])
    def test_invalid_create_cour(self, color):
        test_case = f"color={color}"
        with allure.step(f"Тестовый случай: {test_case}"):
            with allure.step("Подготавливаем данные заказа"):
                or_data = CreateCourier.order
                data = or_data.copy()
                data["color"] = color
            
            with allure.step("Отправляем запрос на создание заказа"):
                response = requests.post(f'{Url.url}{Url.create_order}', json=data)
            
            with allure.step("Проверяем статус код 201"):
                assert response.status_code == 201, f"Ожидался статус 201, но получили {response.status_code}"
            
            with allure.step("Проверяем наличие track в ответе"):
                response_data = response.json()
                assert "track" in response_data, f"Ожидался track в ответе, но получили: {response_data}"
                assert isinstance(response_data["track"], int), f"Track должен быть числом, но получили: {response_data['track']}"
