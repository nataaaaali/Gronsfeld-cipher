import json, hashlib, getpass #для хеширования пароля и пароля, чтобы его не было видно
from models import Change_Text_Request, Delete_Request, One_Text_Request, Cipher_Request, User, Change_Password_Request, Text_Request, Token
from type_of_requests import send_delete, send_get, send_patch, send_post
from error_functions import error1, error2
from text_functions import all_texts, text_one, del_text, text_selection, get_keys, text_verification
from password_verification import get_password
user_token = None  #глобальная переменная для хранения токена

def auth():
    global user_token
    login = input("Введите логин: ")
    password = getpass.getpass("Введите пароль: ")
    user_data = User(login=login, password=password, token='token').model_dump_json().encode('utf-8')
    response = send_post('http://127.0.0.1:8000/auth', data=user_data)
    if not error2(response):  #если ошибка в ответе
        return False
    print(response["message"])
    if isinstance(response, str):
        response = json.loads(response)  #декодирование ответа, если он строка
    user_token = response.get("token")  #сохраняем токен в глобальной переменной
    return True

def registration():
    global user_token
    login = input("Введите логин: ")
    print("Требования к паролю:\n- Пароль должен содержать не менее 10 символов\n- Пароль должен содержать буквы, цифры и спецсимволы")
    password = get_password()
    user_data = User(login = login, password = password, token='token').model_dump_json().encode('utf-8')
    response = send_post('http://127.0.0.1:8000/register', data=user_data)
    if not error2(response):  # Если ошибка в ответе
        return False
    print(response["message"])
    if isinstance(response, str):
        response = json.loads(response)  #декодирование ответа, если он строка
    user_token = response.get("token")  #сохраняем токен в глобальной переменной
    return True

def change_the_password():
    global user_token
    old_password = getpass.getpass("Введите старый пароль: ")
    password = get_password()
    password_request = Change_Password_Request(old_password=old_password, new_password=password, token=user_token).model_dump_json().encode('utf-8')
    response = send_patch('http://127.0.0.1:8000/change_password', data=password_request)
    if not error2(response):  # Если ошибка в ответе
        return False
    print(response["message"])
    new_token = response.get("token") #обновление глобального токен с новым значением
    if new_token:
        user_token = new_token
    return True

def add_text(): #добавление текста
    global user_token
    text = input("Введите текст, который хотите добавить: ")
    text_data = Text_Request(text=text, token=user_token).model_dump_json().encode('utf-8')
    response = send_post('http://127.0.0.1:8000/add_text', data=text_data)  # Отправляем запрос
    if not error2(response):
        return False
    print(response["message"])

def view_all(): #просмотр всех текстов пользователя
    user = Token(token=user_token).model_dump_json().encode('utf-8')
    active = True
    while active:  # Цикл для выбора действия
        print("1. Просмотреть добавленные тексты\n2. Просмотреть зашифрованные тексты\n3. Просмотреть расшифрованные тексты\n4. Назад")
        try:
            number = int(input("Выберите действие: "))
            if number == 1:
                text = all_texts(url='http://127.0.0.1:8000/view_all_texts', user=user, header="Тексты:")
                if not text_verification(text):
                    continue  # Повторить выбор действия
            elif number == 2:
                text = all_texts(url='http://127.0.0.1:8000/view_encrypted_texts', user=user, header="Зашифрованные тексты:")
                if not text_verification(text):
                    continue  # Повторить выбор действия
            elif number == 3:
                text = all_texts(url='http://127.0.0.1:8000/view_decrypted_texts', user=user,header="Расшифрованные тексты:")
                if not text_verification(text):
                    continue  # Повторить выбор действия
            elif number == 4:
                active = False
                return active
            else:
                print("Неверная команда! Введите одно из указанных действий.")
                continue  # Повторить запрос
        except ValueError:
            print("Неверная команда! Введите одно из указанных действий")
            continue  # Повторить запрос
        return True

def view_one_texts():  # просмотр одного текста пользователя
    user = Token(token=user_token).model_dump_json().encode('utf-8')
    active = True
    while active:  #цикл для выбора действия
        print("1. Просмотреть текст из добавленных\n2. Просмотреть текст из зашифрованных\n3. Просмотреть текст из расшифрованных\n4. Назад")
        try:
            command = input("Выберите действие: ")
            if command == "1":  # Исправлено на строку
                type = "user_text"
                text = text_one(url = 'http://127.0.0.1:8000/view_all_texts', user=user)
                if not text_verification(text):
                    continue  # Повторить выбор действия
            elif command == "2":
                type = "encrypted_text"
                text = text_one(url='http://127.0.0.1:8000/view_encrypted_texts', user=user)
                if not text_verification(text):
                    continue  # Повторить выбор действия
            elif command == "3":
                type = "decrypted_text"
                text = text_one(url='http://127.0.0.1:8000/view_decrypted_texts', user=user)
                if not text_verification(text):
                    continue  # Повторить выбор действия
            elif command == "4":
                active = False
                return active
            one_text = One_Text_Request(token=user_token, text_number=text, type = type).model_dump_json().encode('utf-8') # Получаем текст
            response = send_get('http://127.0.0.1:8000/view_one_text', data=one_text)
            if not error1(response):
                return False
            selected_text = response.get('text', "Текст не найден.")
            print(f"Выбранный текст: {selected_text}")
            return True
        except ValueError:
            print("Неверная команда! Введите одно из указанных действий.")

def delete_text(): #удаление текста
    user = Token(token=user_token).model_dump_json().encode('utf-8')
    active = True
    while active:
        print("1. Удалить добавленный текст\n2. Удалить зашифрованный текст\n3. Удалить расшифрованный текст\n4. Назад")
        try:
            command = input("Выберите действие: ")
            if command == "1":
                type = "user_text"
                text = del_text(url='http://127.0.0.1:8000/view_all_texts', user=user, header="Тексты:")
                if not text_verification(text):
                    continue  # Повторить выбор действия
            elif command == "2":
                type = "encrypted_text"
                text = del_text(url='http://127.0.0.1:8000/view_encrypted_texts', user=user, header="Зашифрованные тексты:")
                if not text_verification(text):
                    continue  # Повторить выбор действия
            elif command == "3":
                type = "decrypted_text"
                text = del_text(url='http://127.0.0.1:8000/view_decrypted_texts', user=user, header="Расшифрованные тексты:")
                if not text_verification(text):
                    continue  # Повторить выбор действия
            elif command == "4":
                active = False
                return active
            while True:  # выбор текста для удаления
                try:
                    text_index = int(input("Введите номер текста, который хотите удалить: ")) - 1
                    if 0 <= text_index < len(text):  # Проверка корректности индекса
                        delete = Delete_Request(token=user_token, text_number=text_index, type=type).model_dump_json().encode('utf-8')
                        response = send_delete('http://127.0.0.1:8000/delete_text', data=delete)
                        if not error2(response):  # Если ошибка в ответе
                            return False
                        print(response["message"])
                        return True
                    else:
                        print(f"Введите номер от 1 до {len(text)}.")
                except ValueError:
                    print("Введите корректный номер текста.")
        except ValueError:
            print("Неверная команда! Введите одно из указанных действий.")

def change_the_text(): #изменение текста
    user = Token(token=user_token).model_dump_json().encode('utf-8')
    response = send_get('http://127.0.0.1:8000/view_all_texts', data=user)
    if not error1(response):
        return False
    print("Тексты:")
    texts = response.get('texts', [])
    for index, text_info in enumerate(texts, start=1):
        print(f"{index}. {text_info['content']}")
    while True: #выбор текста для удаления
        try:
            text_number = int(input("Введите номер текста, который хотите изменить: "))
            if 1 <= text_number <= len(texts):  # Проверка корректности индекса
                new_text = input("Введите новй текст: ")
                change_text = Change_Text_Request(token=user_token, text_number=text_number, new_text = new_text).model_dump_json().encode('utf-8')
                response = send_patch('http://127.0.0.1:8000/change_the_text', data = change_text)
                if not error2(response):
                    return False
                print(response["message"])
                return True
            else:
                print(f"Введите номер от 1 до {len(texts)}.")
        except ValueError:
            print("Введите корректный номер текста.")

def encrypt_text():
    user = Token(token=user_token).model_dump_json().encode('utf-8')
    active = True
    while active:  # Цикл для выбора действия
        print("1. Выбрать текст из добавленных\n2. Ввести текст вручную\n3. Назад")
        try:
            command = int(input("Выберите действие: "))
            if command == 1:
                text = text_selection(url='http://127.0.0.1:8000/view_all_texts', user=user, header="Тексты:", action="зашифровать")
                if not text_verification(text):
                    continue  # Повторить выбор действия
            elif command == 2:
                text = input("Введите текст для шифрования: ")
                if not text.strip():
                    print("Текст не может быть пустым! Попробуйте снова.")
                    continue  # Вернуться к выбору действия
            elif command == 3:
                active = False
                return active
            else:
                print("Неверная команда! Введите одно из указанных действий.")
                continue  # Повторить выбор
        except ValueError:
            print("Неверная команда! Введите одно из указанных действий.")
            continue  # Повторить выбор
        key = get_keys()
        data = Cipher_Request(text=text, key=key, token=user_token).model_dump_json().encode('utf-8')
        response = send_post('http://127.0.0.1:8000/cipher_encrypt', data=data)
        if not error2(response):
            return False
        print("Зашифрованный текст:", response["message"])
        return True

def decrypt_text():
    user = Token(token=user_token).model_dump_json().encode('utf-8')
    active = True
    while active:  # Цикл для выбора действия
        print("1. Выбрать текст из добавленных\n2. Выбрать текст из зашифрованных\n3. Ввести текст вручную\n4. Назад")
        try:
            command = int(input("Выберите действие: "))
            if command == 1:
                text = text_selection(url ='http://127.0.0.1:8000/view_all_texts', user=user, header="Тексты:", action="расшифровать")
                if not text_verification(text):
                    continue  # Повторить выбор действия
            elif command == 2:
                text = text_selection(url='http://127.0.0.1:8000/view_encrypted_texts', user=user, header="Зашифрованные тексты:",
                                      action="расшифровать")
                if not text_verification(text):
                    continue  # Повторить выбор действия
            elif command == 3:
                text = input("Введите текст для дешифрования: ")
                if not text.strip():
                    print("Текст не может быть пустым! Попробуйте снова.")
                    continue  # Вернуться к выбору действия
            elif command == 4:
                active = False
                return active # Выход из функции
            else:
                print("Неверная команда! Введите одно из указанных действий.")
                continue  # Повторить запрос
        except ValueError:
            print("Неверная команда! Введите одно из представленных действий.")
            continue  # Повторить запрос
        key = get_keys()
        data = Cipher_Request(text=text, key=key, token=user_token).model_dump_json().encode('utf-8')
        response = send_post('http://127.0.0.1:8000/cipher_decrypt', data=data)
        if not error2(response):
            return False
        print("Расшифрованный текст:", response["message"])
        return True

def query_history():
    user = Token(token=user_token).model_dump_json().encode('utf-8')
    response = send_get('http://127.0.0.1:8000/query_history', data=user)
    if not error1(response):
        return False
    print("Запросы:")
    requests = response.get('requests', [])
    for index, text_info in enumerate(requests, start=1):
        print(f"{index}. {text_info['content']}")

def delete_query_history(): #удаление текста
    user = Token(token=user_token).model_dump_json().encode('utf-8')
    response = send_delete('http://127.0.0.1:8000/delete_query_history', data=user)
    if not error1(response):  #если ошибка в ответе
        return False
    print(response["message"])
    return True

def exit():
    user = Token(token=user_token).model_dump_json().encode('utf-8')
    response = send_delete('http://127.0.0.1:8000/exit', data=user)
    if not error2(response):  #если ошибка в ответе
        return False
    print(response["message"])

def main():
    authenticated, title, active = False, True, True
    while active:
        try:
            if title:  # Отображаем название только при необходимости
                print("Добро пожаловать в приложение 'Шифр Гросфельда!'")
                title = False  # Сбрасываем флаг после отображения названия
            if not authenticated:  # Меню до авторизации/регистрации
                print("1 - Авторизация\n2 - Регистрация\n3 - Выход")
                command = int(input("Выберите действие: "))
                if command == 1:
                    authenticated = auth()
                elif command == 2:
                    authenticated = registration()
                elif command == 3:
                    print("Выход из программы.")
                    break
                else:
                    print("Неверный ввод. Пожалуйста, выберите команду от 1 до 3.")
            else:  # Меню после авторизации/регистрации
                print("1 - Шифрование текста\n2 - Дешифрование текста\n3 - Добавить текст\n4 - Просмотр всех текстов\n5 - Просмотр одного текста\n6 - Изменить текст\n7 - Удалить текст\n8 - Изменение пароля\n9 - История запросов\n10 - Удалить историю запросов\n11 - Выход")
                command = int(input("Выберите действие: "))
                if command == 1:
                    encrypt_text()
                elif command == 2:
                    decrypt_text()
                elif command == 3:
                    add_text()
                elif command == 4:
                    view_all()
                elif command == 5:
                    view_one_texts()
                elif command == 6:
                    change_the_text()
                elif command == 7:
                    delete_text()
                elif command == 8:
                    change_the_password()
                elif command == 9:
                    query_history()
                elif command == 10:
                    delete_query_history()
                elif command == 11:
                    exit()
                    authenticated, title = False, True  # Возвращаемся к меню авторизации/регистрации
                else:
                    print("Неверно введена команда! Пожалуйста, выберите команду от 1 до 11.")
        except ValueError:
            print("Неверно введена команда!")

if __name__ == "__main__":
    main()