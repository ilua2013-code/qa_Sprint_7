import requests
import allure
from url import Url

class TestGetOrder:
    @allure.title('Тест на проверку получения списка заказов')
    @allure.description('Отправляем GET-Запрос и получаем список заказов')
    def test_get_orders_list(self):
        with allure.step('Отправить GET-запрос для получения списка заказов'):
            response = requests.get(f'{Url.url}{Url.return_list_order}')

        with allure.step('Проверить наличие track в ответе'):
            with allure.step("Проверяем статус код 200"):
                assert response.status_code == 200, f"Ожидался статус 200, но получили {response.status_code}"
            
            with allure.step("Проверяем наличие списка заказов в ответе"):
                response_data = response.json()
                assert "orders" in response_data, "В ответе отсутствует список заказов"
                assert isinstance(response_data["orders"], list), "Поле 'orders' должно быть списком"
