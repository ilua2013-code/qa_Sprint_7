import pytest
import allure
from data import CreateCourier

class TestLoginCourier:
    @allure.title('Авторизация курьера')
    @allure.description('Тест авторизации курьера')
    def test_authorization_courier(self, create_cour, post_cour, delete_cour, authorization_cour):
        with allure.step("Создаем курьера"):
            response, data = create_cour()
            assert response.status_code == 201, f"Ожидался статус 201, но получили {response.status_code}"
            assert response.json() == {'ok': True}, f'Ожидался ответ "ok: True", но получили {response.json()}'
        
        with allure.step("Проверяем авторизацию курьера"):
            id_cour = post_cour(data)
            response1 = authorization_cour(data)
            assert response1.status_code == 200, f"Ожидался статус 200, но получили {response1.status_code}"
            assert response1.json()['id'] == id_cour, f'Ожидался ответ {id_cour} но получили {response1.json()["id"]}'
        
        with allure.step("Удаляем созданного курьера"):
            resp = delete_cour(data)
            assert resp.status_code == 200, f"Ожидался статус 200, но получили {resp.status_code}"
            assert resp.json() == {'ok': True}, f'Ожидался ответ "ok: True", но получили {resp.json()}'

    
    @allure.title('Авторизация с неверным логином')
    def test_invalid_login(self, authorization_cour, create_cour, delete_cour):
        _, or_data = create_cour()
        data = or_data.copy()
        data["login"] = CreateCourier.generation_courier_login()
        
        response = authorization_cour(data)
        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Учетная запись не найдена"}
        resp = delete_cour(or_data)
        assert resp.status_code == 200, f"Ожидался статус 200, но получили {resp.status_code}"
        assert resp.json() == {'ok': True}, f'Ожидался ответ "ok: True", но получили {resp.json()}'

    
    @allure.title('Авторизация с неверным паролем')
    def test_invalid_password(self, authorization_cour, create_cour, delete_cour):
        _, or_data = create_cour()
        data = or_data.copy()
        data["password"] = CreateCourier.generation_courier_password()
        
        response = authorization_cour(data)
        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Учетная запись не найдена"}
        resp = delete_cour(or_data)
        assert resp.status_code == 200, f"Ожидался статус 200, но получили {resp.status_code}"
        assert resp.json() == {'ok': True}, f'Ожидался ответ "ok: True", но получили {resp.json()}'

    
    @allure.title('Авторизация с неверным логином и паролем')
    def test_invalid_login_and_password(self, authorization_cour, create_cour, delete_cour):
        _, or_data = create_cour()
        data = or_data.copy()
        data["login"] = CreateCourier.generation_courier_login()
        data["password"] = CreateCourier.generation_courier_password()
        
        response = authorization_cour(data)
        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Учетная запись не найдена"}
        resp = delete_cour(or_data)
        assert resp.status_code == 200, f"Ожидался статус 200, но получили {resp.status_code}"
        assert resp.json() == {'ok': True}, f'Ожидался ответ "ok: True", но получили {resp.json()}'

        
    
    @allure.title('Авторизация без обязательных полей')
    @allure.description('Тест проверяет авторизацию когда отсутствует логин или пароль')
    @pytest.mark.parametrize("login,password", [
        (None, "valid_password"),  
        ("valid_login", None),    
        (None, None),
    ])
    def test_invalid_create_cour(self, login, password, authorization_cour, create_cour,delete_cour):
        test_case = f"login={login}, password={password}"
        with allure.step(f"Тестовый случай: {test_case}"):
            with allure.step("Создаем курьера"):
                _, or_data = create_cour()
                data = or_data
                del data["firstName"]
                # Модифицируем оба поля согласно тестовому случаю
                data = CreateCourier.invalid_data(data, "login", login)
                data = CreateCourier.invalid_data(data, "password", password)
        
            with allure.step("Отправка запроса и валидация"):
                response = authorization_cour(data)
                assert response.status_code == 400, f"Ожидался статус 400, но получили {response.status_code}"
                assert response.json() == {"code": 400, "message": "Недостаточно данных для входа"}, \
                f'Ожидался ответ {{"code": 400, "message": "Недостаточно данных для входа"}}, но получили {response.json()}'
                with allure.step("Удаляем курьера"):
                    resp = delete_cour(or_data)
                    assert resp.status_code == 200, f"Ожидался статус 200, но получили {resp.status_code}"
                    assert resp.json() == {'ok': True}, f'Ожидался ответ "ok: True", но получили {resp.json()}'
    
    @allure.title('Авторизация с пустыми строками и null значениями')
    @allure.description('Тест проверяет авторизацию с пустыми строками и null значениями')
    @pytest.mark.parametrize("login,password", CreateCourier.parameters)
    def test_login_empty_and_null_values(self, login, password, authorization_cour, create_cour, delete_cour):
        test_case = f"login={login}, password={password}"
        with allure.step(f"Тестовый случай: {test_case}"):
            with allure.step("Создаем курьера"):
                _, or_data = create_cour()
                data = or_data
                del data["firstName"]
            
                data = CreateCourier.invalid_data(data, "login", login)
                data = CreateCourier.invalid_data(data, "password", password)
        
            with allure.step("Отправка запроса и валидация"):
                response = authorization_cour(data)
                assert response.status_code == 400, f"Ожидался статус 400, но получили {response.status_code}"
                assert response.json() == {"code": 400, "message": "Недостаточно данных для входа"}, \
                f'Ожидался ответ {{"code": 400, "message": "Недостаточно данных для входа"}}, но получили {response.json()}'
                with allure.step("Удаляем курьера"):
                    resp = delete_cour(or_data)
                    assert resp.status_code == 200, f"Ожидался статус 200, но получили {resp.status_code}"
                    assert resp.json() == {'ok': True}, f'Ожидался ответ "ok: True", но получили {resp.json()}'