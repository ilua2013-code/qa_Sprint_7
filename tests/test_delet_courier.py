import requests
import allure
from url import Url 

class TestDeleteCourier:

    @allure.title('Удаление курьера без параметров')
    @allure.description('Тест неуспешный запрос без ID возвращает соответствующую ошибку')
    def test_delete_courier_without_parameters(self):
        with allure.step("Отправляем запрос на удаление без параметров"):
            data = {}
            response = requests.delete(f'{Url.url}{Url.del_courier[:-1]}', json=data)
        
        with allure.step("Проверяем ошибку 400"):
            assert response.status_code == 400, f"Ожидался статус 400, но получили {response.status_code}"
            assert response.json() == {"message": "Недостаточно данных для удаления курьера"}, \
                f'Ожидался ответ {{"message": "Недостаточно данных для удаления курьера"}}, но получили {response.json()}'

    @allure.title('Удаление курьера с несуществующим ID')
    @allure.description('Тест неуспешный с несуществующим ID возвращает соответствующую ошибку')
    def test_delete_courier_with_nonexistent_id(self):
        with allure.step("Отправляем запрос на удаление с несуществующим ID"):
            data = {"id": "3000000"}
            response = requests.delete(f'{Url.url}{Url.del_courier[:-1]}', json=data)
        
        with allure.step("Проверяем ошибку 404"):
            assert response.status_code == 404, f"Ожидался статус 404, но получили {response.status_code}"
            assert response.json() == {"message": "Курьера с таким id нет"}, \
                f'Ожидался ответ {{"message": "Курьера с таким id нет"}}, но получили {response.json()}'