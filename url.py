

class Url:
    url = 'https://qa-scooter.praktikum-services.ru/'
    
    # Курьер endpoints
    login_courier = 'api/v1/courier/login'              # POST - авторизация курьера
    create_courier = 'api/v1/courier'                   # POST - создание курьера
    del_courier = 'api/v1/courier/'                      # DELETE - удаление курьера (+id)
    
    # Заказы endpoints  
    create_order = 'api/v1/orders'                      # POST - создание заказа
    return_list_order = 'api/v1/orders'                 # GET - список заказов
    put_order = 'api/v1/orders/accept'                  # PUT - принятие заказа (+id)
    get_order_number = 'api/v1/orders/track?t='             # GET - заказ по номеру 
    put_order_del = 'api/v1/orders/cancel'              # PUT - отмена заказа (+id)
                