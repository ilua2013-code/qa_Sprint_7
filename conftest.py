import pytest
import requests
from url import Url 
from data import CreateCourier
import allure

@pytest.fixture(scope="function")
def create_cour():
    """Фикстура для создания курьера"""
    def cre_cour(data = None):
        with allure.step("Создаем курьера"):
            if data is None:
                data = CreateCourier.generate_unique_courier()
                respons = requests.post(f'{Url.url}{Url.create_courier}', json = data)
                return respons, data
            respons = requests.post(f'{Url.url}{Url.create_courier}', json = data)
            return respons, data
    return cre_cour


@pytest.fixture(scope="function")
def delete_cour():
    """Фикстура для удаления курьера по ID в url"""
    def del_cour(courier_data):
        with allure.step("Получаем ID курьера для удаления"):
            respons_post = requests.post(f'{Url.url}{Url.login_courier}', json=courier_data)
            id_cour = respons_post.json()['id']
        
        with allure.step("Удаляем курьера по ID"):
            respons = requests.delete(f'{Url.url}{Url.del_courier}{id_cour}')
            return respons
    return del_cour


@pytest.fixture(scope="function")
def post_cour():
    """Фикстура для получения ID курьера"""
    def return_id_cour(data):
        with allure.step("Получаем ID курьера через авторизацию"):
            respons_post = requests.post(f'{Url.url}{Url.login_courier}', json=data)
            id_cour = respons_post.json()['id']
            return id_cour
    return return_id_cour


@pytest.fixture(scope="function")
def authorization_cour():
    """Фикстура для авторизации курьера"""
    def aut_cour(data):
        with allure.step("Авторизуем курьера"):
            respons_put = requests.post(f'{Url.url}{Url.login_courier}', json=data)
            return respons_put
    return aut_cour

@pytest.fixture
def prepared_order():
    """Фикстура создает заказ и возвращает его ID и track номер"""
    with allure.step("Создаем тестовый заказ"):
        # 1. Берем данные заказа из data.py
        order_data = CreateCourier.order
        
        # 2. Отправляем запрос на создание заказа
        create_order_response = requests.post(f'{Url.url}{Url.create_order}', json=order_data)
        
        # 3. Получаем track номер из ответа
        track_number = create_order_response.json()["track"]
        
        # 4. Получаем ID заказа по track номеру
        get_order_response = requests.get(f'{Url.url}{Url.get_order_number}{track_number}')
        order_id = get_order_response.json()["order"]['id']
        
        return order_id, track_number 

@pytest.fixture
def return_track_order():
    """Фикстура создает заказ и возвращает track номер"""
    with allure.step("Создаем тестовый заказ"):
        # 1. Берем данные заказа из data.py
        order_data = CreateCourier.order
        
        # 2. Отправляем запрос на создание заказа
        create_order_response = requests.post(f'{Url.url}{Url.create_order}', json=order_data)
        
        # 3. Получаем track номер из ответа
        track_number = create_order_response.json()["track"]
    yield track_number  
    
    # 4. После теста - отменяем заказ
    with allure.step("Отменяем тестовый заказ"):
        cancel_data = {"track": track_number}
        requests.put(f'{Url.url}{Url.put_order_del}', json=cancel_data)



@pytest.fixture
def get_track_order():
    def get_order(data):
        """Фикстура получения заказа по track номер"""
        with allure.step("Получение тестовый заказ"):
            # 1. Отправляем запрос на получение заказа
            create_order_response = requests.get(f'{Url.url}{Url.get_order_number}{data}')
            return create_order_response
    return get_order


@pytest.fixture
def prepared_courier(create_cour, post_cour):
    """Фикстура создает курьера и возвращает его ID"""
    with allure.step("Создаем тестового курьера"):
        # 1.создания курьера
        create_courier_response, courier_data = create_cour()
        
        # 2. Используем фикстуру post_cour для получения ID курьера
        courier_id = post_cour(courier_data)
        
        return courier_id  