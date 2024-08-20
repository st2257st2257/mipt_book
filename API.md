USERS | Все адреса в формате http://127.0.0.1:8088/address, если где-то стоит /adress, читать: http://127.0.0.1:8088/address

**Получение токена авторизации:**
- Адрес: /token
- Тип запроса: POST
- Пример данных: {"username": "test_user", "password": "test_pass"}
- Адрес для тестирования: /test/auth/

**Регистрация пользователя:**
- Адрес: /register
- Тип запроса: POST
- Пример данных: {"username": "test_user", "pass": "test_pass", "email": "example@test.com"}
- Адрес для тестирования: /test/register/

**Получение данных по токену:**
- Адрес: /get-info
- Типо запроса: GET
- Пример данных: headers: {'Authorization': Token 3100dc1de794362ac07f2929042bd455601070b9}
- Адрес для тестирования: /test/get/

**Получение данных классов по токену:**
- API Roles:           /base-info/roles
- API Institute Group: /base-info/institute_group
- API Access:          /base-info/access
- API Preferences:     /base-info/preferences


BACKEND | Все адреса в формате http://127.0.0.1:8000/address, если где-то стоит /adress, читать: http://127.0.0.1:8000/address

**Получение данных классов по токену:**
- API Institute:                 /base-info/institute
- API Building:                  /base-info/building
- API Audience Status:           /base-info/audience_status
- API Audience:                  /base-info/audience
- API Book:                      /base-info/book

**Фильтрация данных классов без токена:**
- API Building: /base-info/building/?name=<audience_name>&institute=<institute_name>
a) name          | Примеры: "512","513","514"
b) institute     | Примеры: "МФТИ", "МГУ"
- API Audience: /base-info/building/?building_name=<building_name>&institute=<institute_name>&status=<Свободно>
a) building_name | Примеры: "ГК", "ЛК", "ВМК"
b) institute     | Примеры: "МФТИ", "МГУ"
c) status        | Примеры: "Свободно", "Занято", "Скоро освободиться", "Отсутствует для бронировани"
