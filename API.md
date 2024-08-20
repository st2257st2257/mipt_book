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
1. API Roles:           /base-info/roles
2. API Institute Group: /base-info/institute_group
3. API Access:          /base-info/access
4. API Preferences:     /base-info/preferences


BACKEND | Все адреса в формате http://127.0.0.1:8000/address, если где-то стоит /adress, читать: http://127.0.0.1:8000/address

**Получение данных классов по токену:**
1. API Institute:                 /base-info/institute
2. API Building:                  /base-info/building
3. API Audience Status:           /base-info/audience_status
4. API Audience:                  /base-info/audience
5. API Book:                      /base-info/book

**Фильтрация данных классов без токена:**
1. API Building: /base-info/building/?name=<audience_name>&institute=<institute_name>
   - name            | Примеры: "512","513","514"
   - institute       | Примеры: "МФТИ", "МГУ"
2. API Audience: /base-info/building/?building_name=<building_name>&institute=<institute_name>&status=<Свободно>
   - building_name   | Примеры: "ГК", "ЛК", "ВМК"
   - institute       | Примеры: "МФТИ", "МГУ"
   - status          | Примеры: "Свободно", "Занято", "Скоро освободиться", "Отсутствует для бронировани"
3. API Book: /base-info/book/?audience_number=123&user=test_user&pair_number=2&building_name=ГК&institute=МФТИ
   - building_name   | Примеры: "ГК", "ЛК", "ВМК"
   - institute       | Примеры: "МФТИ", "МГУ"
   - audience_number | Примеры: "512","513","514"
   - user            | Примеры: "test_user"
   - pair_number     | Примеры: "1", "2", "3"
