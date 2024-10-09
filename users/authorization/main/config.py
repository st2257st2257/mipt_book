# email text configurations for changing username
CHANGE_NAME_TITLE = "Изменение ФИО пользователя"
ADMIN_FOOTER_INFO = "\n\nС уважением,\n" \
                    "Сервис бронирования аудиторий МФТИ\n" \
                    "info@mipt.site\n" \
                    "https://mipt.site"

def get_change_name_text(username, data_request):
    first_name = data_request.get('first_name')
    last_name = data_request.get('last_name')
    third_name = data_request.get('third_name')
    final_data = f"Запрос на изменение имя пользователя успешно выполнен.\n\n" \
                 f"Имя пользователя: {username}" \
                 f"Имя:{first_name}" \
                 f"Фамилия:{last_name}" \
                 f"Отчество:{third_name}\n\n" \
                 f"Подробную информацию можно получить по ссылке: https://mipt.site/info" \
                 f"{ADMIN_FOOTER_INFO}"
    return final_data


# email text configurations user registration

def get_registration_text(username):
    final_data = f"Аккаунт с именем пользователя: {username} был зарегистрирован на сайте https://mipt.site\n\n" \
                 f"Если это были вы, перейдите по ссылке для подтверждения аккаунта: https://mipt.site/proof/ksbd23n\n\n" \
                 f"Если это были не вы, перейдите по ссылке для отмены регистрации: https://mipt.site/cancel/sdfvf43" \
                 f"{ADMIN_FOOTER_INFO}"
    return final_data
