
from faker import Faker
class CreateCourier:
    json_null = object()
    fake = Faker(locale = 'ru_RU')
    
    
    test_data = [
    (None, "12345", json_null),
    (None, None, "Саша"),
    (None, json_null, None),
    (None, "", ""), 
    (json_null, "12345", "Саша"),
    (json_null, None, None),
    (json_null, json_null, ""),
    (json_null, "", json_null),
    (fake.user_name(), "12345", None),
    (fake.user_name(), None, ""),
    (fake.user_name(), json_null, json_null),
    (fake.user_name(), "", "Саша"),
    ("", "12345", ""),
    ("", None, json_null),
    ("", json_null, "Саша"),
    ("", "", None),
    (None, "12345", "Саша"),
    (None, json_null, ""),
    (json_null, "12345", None),
    ("json_null", "", "Саша"),
    (fake.user_name(), "12345", json_null),
    (fake.user_name(), None, "Саша"),
    ("", "12345", json_null),
    ("", json_null, None)
]
    order = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2020-06-06",
    "comment": "Saske, come back to Konoha"
}
  
    
    parameters = [
        ("", "valid_password"),           
        ("valid_login", ""),              
        ("", ""),                         
        (json_null, "valid_password"),         
        ("valid_login", json_null),            
        (json_null, json_null),                   
    ]


    
    @classmethod
    def invalid_data(cls, data, key_value, new_value):
        data = data.copy()
        if new_value is None:
            del data[key_value]
        elif new_value is cls.json_null:
            data[key_value] = None
        else:
            data[key_value] = new_value
        return data
    
    @classmethod
    def generation_courier_login(cls):
        return cls.fake.user_name()
        
    @classmethod
    def generation_courier_password(cls):
        return cls.fake.password()
    
    @classmethod
    def generation_courier_name(cls):
        return cls.fake.first_name()
    
    
    @classmethod
    def generate_unique_courier(cls):
        """Генерация полного уникального курьера"""
        return {
            "login": cls.generation_courier_login(),
            "password": cls.generation_courier_password(),
            "firstName": cls.generation_courier_name()
        }
    