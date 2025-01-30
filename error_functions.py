def error1(response):
    if isinstance(response, dict):
        if "error" in response:  # Если ошибка в ответе
            print("Ошибка:", response["error"])
            return False
        if "message" in response:  # Если есть сообщение о пустой папке
            print(response["message"])
            return False
    return True

def error2(response):
    if isinstance(response, dict) and "error" in response:  # Если ошибка в ответе
        print("Ошибка:", response["error"])
        return False
    return True