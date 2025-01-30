from fastapi import FastAPI, HTTPException
import time, json, os, hashlib,secrets #для хеширования пароля и токена
from models import Change_Text_Request, Delete_Request, One_Text_Request, Cipher_Request, User, Change_Password_Request, Text_Request, Token
from text_functions import gronsfeld_encrypt, gronsfeld_decrypt
from password_verification import complex_password_s
from additional_functions import token_search, login_search, request
app = FastAPI()

@app.post("/register") #регистрация пользователя
def create_user(user: User):
    if not complex_password_s(user.password): #проверка пароля
        raise HTTPException(status_code=409, detail="Неверный пароль!")
    folder_path = 'users'
    os.makedirs(folder_path, exist_ok=True)  #проверка и создание папки
    if login_search(user.login, folder_path):
        raise HTTPException(status_code=409, detail="Пользователь существует.")
    user.id = int(time.time())
    user.token = secrets.token_hex(8) #генерация технического токена
    user.password = hashlib.sha256(user.password.encode()).hexdigest() #хеширование пароля
    with open(f"users/user_{user.id}.json", 'w') as f: #сохранение пользователя
        json.dump(user.dict(), f)
    request(user.id, user.login, f"Регистрация")  #сохранение запроса
    return {"message": "Регистрация успешна!", "token": user.token}

@app.post("/auth") #авторизация пользователя
def authorization(user: User):
    folder_path = 'users'
    tmp_user = login_search(user.login, folder_path) #поиск пользователя по логину
    if not tmp_user:
        raise HTTPException(status_code=409, detail="Пользователь не найден.")
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest() #хеширование пароля и сравнивание его с сохранённым
    if tmp_user['password'] == hashed_password:
        request(tmp_user['id'], tmp_user['login'], f"Авторизация")  # сохранение запроса
        return {"message": "Авторизация успешна!", "token": tmp_user['token']}
    else:
        raise HTTPException(status_code=409, detail="Неверный пароль.")

@app.patch("/change_password") #изменение пароля
def change_the_password(data: Change_Password_Request):
    folder_path = 'users'
    user_found = False
    for json_file in os.listdir(folder_path):
        if json_file.endswith('.json'):
            file_path = os.path.join(folder_path, json_file)
            with open(file_path, 'r') as f:
                tmp_user = json.load(f)
            if tmp_user['token'] == data.token:
                if tmp_user['password'] != hashlib.sha256(data.old_password.encode()).hexdigest():
                    raise HTTPException(status_code=401, detail="Неверный старый пароль.")
                tmp_user['password'] = hashlib.sha256(data.new_password.encode()).hexdigest()
                new_token = secrets.token_hex(8)
                tmp_user['token'] = new_token
                with open(file_path, 'w') as fw:
                    json.dump(tmp_user, fw)
                return {"message": "Пароль успешно изменён.", "token": new_token}
    if not user_found:
        raise HTTPException(status_code=409, detail="Пользователь не найден.")

@app.post("/add_text")  #добавление текста
def add_text2(text: Text_Request):
    user_id, user_login = token_search(text.token)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    folder_path = 'user_text'  # проверка и создание папки для текстов
    user_folder = os.path.join(folder_path, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    current_time = int(time.time())
    file_name = f"text_{current_time}.txt"
    file_path = os.path.join(user_folder, file_name)  # добавление текста в файл
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text.text)
    request(user_id, user_login, f"Добавление текста") #сохранение запроса
    return {"message": "Текст успешно добавлен!"}

@app.get("/view_all_texts")  #просмотр всех текстов пользователя
def view_all_texts(token: Token):
    user_id, user_login = token_search(token.token)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    folder_path = 'user_text'
    user_folder = os.path.join(folder_path, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    if not os.path.exists(user_folder):  # проверка на существование папки и наличие файлов
        request(user_id, user_login, f"Просмотр всех добавленных текстов")  # сохранение запроса
        raise HTTPException(status_code=404, detail="Нет текстов для пользователя")
    if not os.listdir(user_folder):  #если папка существует, но пуста
        request(user_id, user_login, f"Просмотр всех добавленных текстов")  # сохранение запроса
        return {"message": "У вас нет добавленных текстов."}

    all_texts = []
    for file_name in os.listdir(user_folder): #чтение текстов из папки пользователя
        file_path = os.path.join(user_folder, file_name)
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            all_texts.append({"content": content})
    request(user_id, user_login, f"Просмотр всех добавленных текстов")  # сохранение запроса
    return {"texts": all_texts}

@app.get("/view_encrypted_texts")  #просмотра зашифрованных текстов пользователя
def view_encrypted_text(token: Token):
    user_id, user_login =token_search(token.token)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    folder_path = 'encrypted_text'
    user_folder = os.path.join(folder_path, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    if not os.path.exists(user_folder): #проверка на существование папки и наличие файлов
        request(user_id, user_login, f"Просмотр всех зашифрованных текстов")  # сохранение запроса
        raise HTTPException(status_code=404, detail="Нет текстов для пользователя")
    if not os.listdir(user_folder):  #если папка существует, но пуста
        request(user_id, user_login, f"Просмотр всех зашифрованных текстов")  # сохранение запроса
        return {"message": "У вас нет зашифрованных текстов."}
    encrypted_texts = []
    for file_name in os.listdir(user_folder): #чтение текстов из папки пользователя
        file_path = os.path.join(user_folder, file_name)
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            encrypted_texts.append({"content": content})
    request(user_id, user_login, f"Просмотр всех зашифрованных текстов")  # сохранение запроса
    return {"texts": encrypted_texts }

@app.get("/view_decrypted_texts")  #просмотра расшифрованных текстов пользователя
def view_decrypted_text(token: Token):
    user_id, user_login = token_search(token.token)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    folder_path = 'decrypted_text'
    user_folder = os.path.join(folder_path, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    if not os.path.exists(user_folder): #проверка на существование папки и наличие файлов
        request(user_id, user_login, f"Просмотр всех расшифрованных текстов")  # сохранение запроса
        raise HTTPException(status_code=404, detail="Нет текстов для пользователя") #НУЖНО ИЗМЕНИТЬ НАДПИСИ НА БОЛЕЕ КОРРЕКТНЫЕ
    if not os.listdir(user_folder):  #если папка существует, но пуста
        request(user_id, user_login, f"Просмотр всех расшифрованных текстов")  # сохранение запроса
        return {"message": "У вас нет расшифрованных текстов."}
    decrypted_texts = []
    for file_name in os.listdir(user_folder): #чтение текстов из папки пользователя
        file_path = os.path.join(user_folder, file_name)
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            decrypted_texts.append({"content": content})
    request(user_id, user_login, f"Просмотр всех расшифрованных текстов")  # сохранение запроса
    return {"texts": decrypted_texts }

@app.get("/view_one_text")  #просмотр одного текста пользователя
def view_one_text(text: One_Text_Request):
    user_id, user_login = token_search(text.token)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user_folder = os.path.join(text.type, str(user_id))
    if not os.path.exists(user_folder):  # Проверка на существование папки
        request(user_id, user_login, f"Просмотр одного текста")  # сохранение запроса
        raise HTTPException(status_code=404, detail="Нет текстов для пользователя")
    if not os.listdir(user_folder):  # если папка существует, но пуста
        request(user_id, user_login, f"Просмотр одного текста")  # сохранение запроса
        return {"message": "У вас нет добавленных текстов."}
    text_files = os.listdir(user_folder)  # Получение списка файлов
    if text.text_number < 0 or text.text_number > len(text_files):
        raise HTTPException(status_code=400, detail=f"Выберите номер от 1 до {len(text_files)}")
    selected_file = text_files[text.text_number - 1]  # Индексация с 0
    file_path = os.path.join(user_folder, selected_file)
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
    request(user_id, user_login, f"Просмотр одного текста")  # сохранение запроса
    return {"text": content}

@app.delete("/delete_text")  #удаление текста
def delete_text(text: Delete_Request):
    user_id, user_login = token_search(text.token)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user_folder = os.path.join(text.type, str(user_id))
    if not os.path.exists(user_folder):  # Проверка на существование папки
        request(user_id, user_login, f"Удаление текста")  # сохранение запроса
        raise HTTPException(status_code=404, detail="Нет текстов для пользователя")
    if not os.listdir(user_folder):  # если папка существует, но пуста
        request(user_id, user_login, f"Просмотр одного текста")  # сохранение запроса
        return {"message": "У вас нет текстов для удаления."}
    files = os.listdir(user_folder)
    if text.text_number < 0 or text.text_number > len(files):
        raise HTTPException(status_code=404, detail="Текст с указанным номером не найден")
    file_to_delete = os.path.join(user_folder, files[text.text_number]) #удаление выбранного файла
    os.remove(file_to_delete)
    request(user_id, user_login, f"Удаление текста")  # сохранение запроса
    return {"message": "Текст успешно удалён"}

@app.patch("/change_the_text") #изменение текста
def change_the_text(text: Change_Text_Request):
    user_id, user_login = token_search(text.token)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user_folder = os.path.join('user_text', str(user_id))  # получение списка файлов пользователя
    if not os.path.exists(user_folder) or not os.listdir(user_folder):
        request(user_id, user_login, f"Изменение текста")  # сохранение запроса
        raise HTTPException(status_code=404, detail="Нет доступных текстов для изменения")
    files = os.listdir(user_folder)
    if text.text_number < 1 or text.text_number > len(files):
        raise HTTPException(status_code=404, detail="Текст с указанным номером не найден")
    if not text.new_text.strip():
        raise HTTPException(status_code=400, detail="Новый текст не может быть пустым")
    file_to_update = os.path.join(user_folder, files[text.text_number - 1])
    with open(file_to_update, 'w', encoding="utf-8") as f: #обновление текста в файле
        f.write(text.new_text)
    request(user_id, user_login, f"Изменение текста")  # сохранение запроса
    return {"message": "Текст успешно обновлён"}

@app.post("/cipher_encrypt") #запрос на шифрование
def encrypt(data: Cipher_Request):
    user_id, user_login = token_search(data.token)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not data.text:  # Если текст не передан, проверяем наличие текстов у пользователя
        user_folder = os.path.join('user_text', str(user_id))
        if not os.path.exists(user_folder) or not os.listdir(user_folder):
            request(user_id, user_login, f"Шифрование текста")
            raise HTTPException(status_code=404, detail="Нет доступных текстов для пользователя")
    encrypted_text = gronsfeld_encrypt(data.text, data.key)
    folder_path = "encrypted_text"
    os.makedirs(folder_path, exist_ok=True)
    user_folder = os.path.join(folder_path, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    text_id = int(time.time())
    file_path = os.path.join(user_folder, f"text_{text_id}.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(encrypted_text)
    request(user_id, user_login, f"Шифрование текста")  # сохранение запроса
    return {"message": encrypted_text}

@app.post("/cipher_decrypt")  #запрос на дешифрование
def decrypt(data: Cipher_Request):
    user_id, user_login = token_search(data.token)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not data.text:  # Если текст не передан, проверяем наличие текстов у пользователя
        user_folder = os.path.join('user_text', str(user_id))
        if not os.path.exists(user_folder) or not os.listdir(user_folder):
            request(user_id, user_login, f"Шифрование текста")
            raise HTTPException(status_code=404, detail="Нет доступных текстов для пользователя")
    decrypted_text = gronsfeld_decrypt(data.text, data.key)
    folder_path = "decrypted_text"
    os.makedirs(folder_path, exist_ok=True)
    user_folder = os.path.join(folder_path, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    text_id = int(time.time())
    file_path = os.path.join(user_folder, f"text_{text_id}.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(decrypted_text)
    request(user_id, user_login, f"Дешифрование текста")  # сохранение запроса
    return {"message": decrypted_text}

@app.get("/query_history") #просмотр истории запросов пользователя
def view_query_history(token: Token):
    user_id, user_login = token_search(token.token)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    folder_path = 'query_history'
    os.makedirs(folder_path, exist_ok=True)
    user_folder = os.path.join(folder_path, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    if not os.path.exists(user_folder):  # проверка на существование папки и наличие файлов
        request(user_id, user_login, f"История запросов пользователя")  # сохранение запроса
        raise HTTPException(status_code=404, detail="Нет запросов пользователя")
    if not os.listdir(user_folder):  #если папка существует, но пуста
        request(user_id, user_login, f"История запросов пользователя")  # сохранение запроса
        return {"message": "У вас нет истории запросов ."}
    requests = []
    for file_name in os.listdir(user_folder): #чтение текстов из папки пользователя
        file_path = os.path.join(user_folder, file_name)
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            requests.append({"content": content})
    request(user_id, user_login, f"История запросов пользователя")  # сохранение запроса
    return {"requests": requests}

@app.delete("/delete_query_history") #удаление истории запросов
def delete_query_history(token: Token):
    user_id, user_login = token_search(token.token)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    folder_path = 'query_history'
    os.makedirs(folder_path, exist_ok=True)
    user_folder = os.path.join(folder_path, str(user_id))
    os.makedirs(folder_path, exist_ok=True)
    if not os.path.exists(user_folder):
        request(user_id, user_login, f"Удаление истории запросов пользователя")  # сохранение запрос
        raise HTTPException(status_code=404, detail="Нет истории запросов пользователя")
    for file_name in os.listdir(user_folder):
        file_path = os.path.join(user_folder, file_name)
        os.remove(file_path)
    request(user_id, user_login, f"Удаление истории запросов пользователя")  # сохранение запроса
    return {"message": "История запросов успешно удалена."}

@app.delete("/exit") #выход из программы
def exit(data: Token):
    user_id, user_login = token_search(data.token)
    if user_id is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    request(user_id, user_login, f"Выход из программы")  # сохранение запроса
    return {"message": "До новых встреч!\n"}