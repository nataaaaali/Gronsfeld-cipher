import getpass

def get_password():
    while True:
        password = getpass.getpass("Введите пароль: ")
        password_confirm = getpass.getpass("Подтвердите пароль: ")
        if password != password_confirm:
            print("Пароли не совпадают! Попробуйте снова.")
            continue
        if not complex_password(password):
            continue
        return password

def complex_password(password): #проверка пароля на сложность на стороне клиена
    if len(password) < 10:
        print("Пароль должен быть не менее 10 символов. Попробуйте снова.")
        return False
    if not any(char.isalpha() for char in password):
        print("Пароль должен содержать буквы. Попробуйте снова.")
        return False
    if not any(char.isdigit() for char in password):
        print("Пароль должен цифры. Попробуйте снова.")
        return False
    if not any(char in "!@#$%^&*()_-+=<>?/:;.,~" for char in password):
        print("Пароль должен содержать специальные символы. Попробуйте снова.")
        return False
    return True

def complex_password_s(password: str) -> bool: #проверка пароля на сложность на сервере
    min_length = len(password) >= 10 #длина
    letters = any(char.isalpha() for char in password) #буквы
    digits = any(char.isdigit() for char in password)  #цифры
    special_char = any(char in "!@#$%^&*()_-+=<>?/:;.,~" for char in password) #спецсимволы
    return min_length and letters and digits and special_char