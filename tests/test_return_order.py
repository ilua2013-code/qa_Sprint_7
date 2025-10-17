import requests
import allure
from url import Url 

class TestReturnOrder:
    def test_accept_order_by_courier(self, prepared_order, prepared_courier):
        with allure.step("Принять заказ курьером"):
            order_id, track_number = prepared_order
            courier_id = prepared_courier
            
            response = requests.put(f'{Url.url}{Url.put_order}/{order_id}?courierId={courier_id}')
            
            assert response.status_code == 200
            assert response.json() == {'ok': True}

    def test_accept_order_without_courier_id(self, prepared_order):
        with allure.step("Принять заказ не передавая id курьера"):
            order_id, _ = prepared_order
            resp = requests.put(f'{Url.url}{Url.put_order}/{order_id}') 

            assert resp.status_code == 400, f"Ожидался статус 400, но получили {resp.status_code}"
            assert resp.json() == {"message": "Недостаточно данных для поиска"}, \
            f'Ожидался ответ {{"message": "Недостаточно данных для поиска"}}, но получили {resp.json()}'

    def test_accept_order_with_invalid_courier_id(self, prepared_order):
        with allure.step("Принять заказ с неверным id курьера"):
            order_id, _ = prepared_order
            resp = requests.put(f'{Url.url}{Url.put_order}/{order_id}?courierId=999999')  # Неверный ID курьера

            assert resp.status_code == 404, f"Ожидался статус 404, но получили {resp.status_code}"
            assert resp.json() == {"message": "Курьера с таким id не существует"}, \
            f'Ожидался ответ {{"message": "Курьера с таким id не существует"}}, но получили {resp.json()}'

    def test_accept_order_without_order_id(self, prepared_courier):
        with allure.step("Принять заказ не передавая id заказа"):
            resp = requests.put(f'{Url.url}{Url.put_order}/?courierId={prepared_courier}')  # Без order_id

            assert resp.status_code == 400, f"Ожидался статус 400, но получили {resp.status_code}"
            assert resp.json() == {"message": "Недостаточно данных для поиска"}, \
            f'Ожидался ответ {{"message": "Недостаточно данных для поиска"}}, но получили {resp.json()}'

    def test_accept_order_with_invalid_order_id(self, prepared_courier):
        with allure.step("Принять заказ с неверным id заказа"):
            resp = requests.put(f'{Url.url}{Url.put_order}/888888?courierId={prepared_courier}')  # Неверный ID заказа

            assert resp.status_code == 404, f"Ожидался статус 404, но получили {resp.status_code}"
            assert resp.json() == {"message": "Заказа с таким id не существует"}, \
        f'Ожидался ответ {{"message": "Заказа с таким id не существует"}}, но получили {resp.json()}'