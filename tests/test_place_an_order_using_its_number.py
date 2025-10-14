import allure

class TestGetOrder:

    @allure.title('Получение заказа по номеру')
    @allure.description('Успешное получение заказа по корректному номеру трека')
    def test_get_order_by_valid_track_number(self, return_track_order, get_track_order):
        with allure.step("Успешный запрос возвращает объект с заказом"):
            track = return_track_order
            create_order_response = get_track_order(track)  
            
            assert create_order_response.status_code == 200, (
                f"Ожидался статус код 200, но получили {create_order_response.status_code}. "
                f"Ответ: {create_order_response.text}"
            )
            
            response_data = create_order_response.json()
            assert 'order' in response_data, (
                f"В ответе отсутствует поле 'order'. Полный ответ: {response_data}"
            )
            
            assert 'track' in response_data["order"], (
                f"В объекте заказа отсутствует поле 'track'."
                f"Данные заказа: {response_data['order']}"
            )

    @allure.title('Получение заказа без номера')
    @allure.description('Запрос заказа без номера трека возвращает ошибку')
    def test_get_order_with_empty_track_number(self, get_track_order):
        with allure.step("Запрос без номера возвращает ошибку"):
            create_order_response = get_track_order('')  
            assert create_order_response.status_code == 400, (
                f"Ожидался статус код 400, но получили {create_order_response.status_code}. "
                f"Ответ: {create_order_response.text}")
            assert create_order_response.json() == {"message":  "Недостаточно данных для поиска"}, (
            f'Ожидался ответ {{"message":  "Недостаточно данных для поиска"}}, '
            f'но получили {create_order_response.json()}')

    
    @allure.title('Получение заказа с несуществующим номером')
    @allure.description('Запрос заказа с несуществующим номером трека возвращает ошибку')
    def test_get_order_with_invalid_track_number(self, get_track_order):
        with allure.step("Запрос с несуществующим номером возвращает ошибку"):
            create_order_response = get_track_order(10000000)  
            assert create_order_response.status_code == 404, (
                f"Ожидался статус код 404, но получили {create_order_response.status_code}. "
                f"Ответ: {create_order_response.text}")
            assert create_order_response.json() == {"message": "Заказ не найден"}, (
            f'Ожидался ответ {{"message": "Заказ не найден"}}, '
            f'но получили {create_order_response.json()}')