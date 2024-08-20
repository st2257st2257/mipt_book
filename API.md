USERS

**Получение токена авторизации:**
- Адрес: http://127.0.0.1:8088/token
- Тип запроса: POST
- Пример данных: {"username": "test_user", "password": "test_pass"}
- Адрес для тестирования: http://127.0.0.1:8088/test/auth/

**Регистрация пользователя:**
- Адрес: http://127.0.0.1:8088/register
- Тип запроса: POST
- Пример данных: {"username": "test_user", "pass": "test_pass", "email": "example@test.com"}
- Адрес для тестирования: http://127.0.0.1:8088/test/register/

**Получение данных по токену:**
- Адрес: http://127.0.0.1:8088/get-info
- Типо запроса: GET
- Пример данных: headers: {'Authorization': Token 3100dc1de794362ac07f2929042bd455601070b9}
- Адрес для тестирования: http://127.0.0.1:8088/test/get/

**Получение данных классов по токену:**
- API Roles:           http://127.0.0.1:8088/base-info/roles
- API Institute Group: http://127.0.0.1:8088/base-info/institute_group
- API Access:          http://127.0.0.1:8088/base-info/access
- API Preferences:     http://127.0.0.1:8088/base-info/preferences


BACKEND

**Получение данных классов по токену:**
- API Institute:           http://127.0.0.1:8000/base-info/institute
- API Building:           http://127.0.0.1:8000/base-info/building
- API Audience Status:           http://127.0.0.1:8000/base-info/audience_status
- API Audience:           http://127.0.0.1:8000/base-info/audience
- API Book:           http://127.0.0.1:8000/base-info/book

**Фильтрация данных классов по токену:**
- API Building: http://127.0.0.1:8000/base-info/building/?name=<aud_name>&institute=<institute_name>
