import requests
import pytest
import allure
from url import Url 
from data import CreateCourier

class TestCreatingCourier:

    @allure.title('Создание курьера')
    @allure.description('Тест успешное создание курьера')
    def test_create_courier(self, create_cour, delete_cour):
        with allure.step("Создаем нового курьера"):
            response, data = create_cour()
    
        with allure.step("Проверяем что курьер создан успешно (статус 201)"):
            assert response.status_code == 201, f"Ожидался статус 201, но получили {response.status_code}"
            assert response.json() == {'ok': True}, f'Ожидался ответ "ok: True", но получили {response.json()}'
    
        with allure.step("Удаляем созданного курьера"):
            resp = delete_cour(data)
            assert resp.status_code == 200, f"Ожидался статус 200, но получили {resp.status_code}"
            assert resp.json() == {'ok': True}, f'Ожидался ответ "ok: True", но получили {resp.json()}'


    @allure.title('Создание курьера с дублирующими данными')
    @allure.description('Тест создание курьера с теми же данными')
    def test_create_duplicate_courier(self, create_cour, delete_cour):
        with allure.step("Создаем первого курьера"):
            response, data = create_cour()
            assert response.status_code == 201, f"Ожидался статус 201, но получили {response.status_code}"
            assert response.json() == {'ok': True}, f'Ожидался ответ "ok: True", но получили {response.json()}'
    
        with allure.step("Пытаемся создать второго курьера с теми же данными"):
            dup_response, dup_data = create_cour(data=data)
            assert dup_response.status_code == 409, (
                f"При создании дубликата ожидался статус 409, но получили {dup_response.status_code}."
                f"Ответ: {dup_response.text}")
    
        with allure.step("Удаляем первого курьера"):
            resp = delete_cour(data)
            assert resp.status_code == 200, f"Ожидался статус 200, но получили {resp.status_code}"
            assert resp.json() == {'ok': True}, f'Ожидался ответ "ok: True", но получили {resp.json()}'


    @allure.title('Создание курьера: отсутствие полей, пустые значения и null')
    @allure.description('Тест негативное тестирование создания курьера. Проверяются варианты: отсутствие полей, передача пустых строк, установка null значений')
    @pytest.mark.parametrize("login, password, first_name", CreateCourier.test_data)
    def test_invalid_create_cour(self, login, password, first_name):
        test_case = f"login={login}, password={password}, first_name={first_name}"
    
        with allure.step(f"Тестовый случай: {test_case}"):
            with allure.step("Генерируем и модификация уникальные данные курьера"):
                data = CreateCourier.generate_unique_courier()
                data = CreateCourier.invalid_data(data, "login", login)
                data = CreateCourier.invalid_data(data, "password", password)
                data = CreateCourier.invalid_data(data, "firstName", first_name)
    
            with allure.step("Отправка запроса и валидация"):
                response = requests.post(f'{Url.url}{Url.create_courier}', json=data)
                assert response.status_code == 400, f"Ожидался статус 400, но получили {response.status_code}"
                assert response.json() == {"code": 400,"message": "Недостаточно данных для создания учетной записи"}, \
                f'Ожидался ответ {{"code": 400, "message": "Недостаточно данных для создания учетной записи"}}, но получили {response.json()}'


    @allure.title('Создание курьера с существующим логином')
    @allure.description('Тест создание курьера с существующем логином')
    def test_create_duplicate_login(self, create_cour, delete_cour):
        
        with allure.step("Создаем первого курьера"):
            response, orig_data = create_cour()
            assert response.status_code == 201, f"Ожидался статус 201, но получили {response.status_code}"
    
        with allure.step("Создаем копию данных с новым паролем и именем, но тем же логином"):
            data = orig_data.copy()
            data['password'] = CreateCourier.generation_courier_password()
            data["firstName"] = CreateCourier.generation_courier_name()
    
        with allure.step("Пытаемся создать второго курьера с существующим логином"):
            new_response, _ = create_cour(data=data)
            assert new_response.status_code == 409, f"Ожидался статус 409, но получили {new_response.status_code}"
    
        with allure.step("Удаляем первого курьера с оригинальными данными"):
            resp = delete_cour(orig_data)
            assert resp.status_code == 200, f"Ожидался статус 200, но получили {resp.status_code}"
        
        