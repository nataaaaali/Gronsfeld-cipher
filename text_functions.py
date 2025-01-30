from type_of_requests import send_get
from error_functions import error1
from typing import List

def text_selection(url: str, user: bytes, header: str, action: str) -> str: #для выбора текста
    response = send_get(url, data=user)
    if not error1(response):
        return ""  #возвращается пустая строка
    texts = response.get('texts', [])
    if not texts:
        return "" #возвращается пустая строка
    print(header)
    for index, text_info in enumerate(texts, start=1):
        print(f"{index}.{text_info['content']}")
    while True:
        try:
            text_number = int(input(f"Введите номер текста, который хотите {action}: "))
            if 1 <= text_number <= len(texts):  # Проверка диапазона
                return texts[text_number - 1]['content']
            else:
                print(f"Введите номер от 1 до {len(texts)}.")
        except ValueError:
            print("Введите корректный номер текста.")

def all_texts(url:str, user:bytes, header:str):
    response = send_get(url=url, data=user)
    if not error1(response):
        return False
    print(header)
    texts = response.get('texts', [])
    for index, text_info in enumerate(texts, start=1):
        print(f"{index}. {text_info['content']}")

def text_one(url: str, user: bytes): #для просмотра одного текста
    response = send_get(url, data=user)
    if not error1(response):
        return False
    texts = response.get('texts', [])  # получение количество текстов
    text_count = len(texts)
    print(f"У вас есть {text_count} текстов.")  # выбор текста
    while True:
        try:
            text_number = int(input(f"Выберете номер текста от 1 до {text_count}: "))
            if 1 <= text_number <= text_count:
                return text_number
            else:
                print(f"Введите число от 1 до {text_count}.")
        except ValueError:
            print("Введите корректное число.")

def del_text(url:str, user:bytes, header:str): #для удаления текста
    response = send_get(url=url, data=user)
    if not error1(response):
        return False
    print(header)
    texts = response.get('texts', [])
    for index, text_info in enumerate(texts, start=1):
        print(f"{index}. {text_info['content']}")
    return texts

def get_keys():
    while True:  #повторение ввода ключей до корректного значения
        try:
            key = list(map(int, input("Введите ключи через пробел: ").split()))
            return key  #возвращает корректно введенные ключи
        except ValueError:
            print("Ошибка: ключи должны быть целыми числами.")

def text_verification(text):
    if not text:  #если пустая строка
        print("Выберите, пожалуйста,другое действие.")
        return False
    return True

def gronsfeld_encrypt(text: str, key: List[int]) -> str:
    alphabets = [
        'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
        'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'abcdefghijklmnopqrstuvwxyz',
    ]
    key_len = len(key)
    result = [] #для хранения зашифрованных символов
    for i, char in enumerate(text):
        for alphabet in alphabets:
            if char in alphabet:
                shift = key[i % key_len] #определение сдвига
                index_char = alphabet.index(char)
                new_char = alphabet[(index_char + shift) % len(alphabet)]
                result.append(new_char)
                break
        else:
            result.append(char)  #если символ не в алфавитах, добавляем как есть

    return ''.join(result) #преобразование в строку

def gronsfeld_decrypt(text: str, key: list[int]) -> str:
    alphabets = [
        'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
        'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'abcdefghijklmnopqrstuvwxyz',
    ]
    key_len = len(key)
    result = [] #для хранения расшифрованных символов
    for i, char in enumerate(text):
        for alphabet in alphabets:
            if char in alphabet:
                shift = key[i % key_len] #определение сдвига
                index_char = alphabet.index(char)
                new_char = alphabet[(index_char - shift) % len(alphabet)]
                result.append(new_char)
                break
        else:
            result.append(char)  #если символ не в алфавитах, добавляем как есть

    return ''.join(result) #преобразование в строку
