import unittest
import requests
import json

class Test1(unittest.TestCase):
    def test_register(self):
        self.login = "User1"
        self.password = "Password12345.."
        data = json.dumps({"login": self.login, "password": self.password, "token": 'token'}).encode('utf-8')
        try:
            response = requests.post("http://127.0.0.1:8000/register", data=data)
        except requests.exceptions.RequestException as e:
            self.fail(f"Ошибка при отправке запроса: {e}")
        response_json = response.json()
        self.token = response_json.get("token")
        print()
        print(response.json().get("message"))

class Test2(unittest.TestCase):
    def test_auth(self):
        self.login = "User2"
        self.password = "Password12345.."
        data = json.dumps({"login": self.login, "password": self.password, "token": 'token'}).encode('utf-8')
        response = requests.post("http://127.0.0.1:8000/register", data=data)
        response_json = response.json()
        self.token = response_json.get("token")
        data = json.dumps({"login": self.login, "password": self.password, "token": self.token}).encode('utf-8')
        try:
            response = requests.post("http://127.0.0.1:8000/auth", data=data)
        except requests.exceptions.RequestException as e:
            self.fail(f"Ошибка при отправке запроса: {e}")
        print()
        print(response.json().get("message"))

class Test3(unittest.TestCase):
    def test_encrypt_text(self):
        self.login = "User2"
        self.password = "Password12345.."
        data = json.dumps({"login": self.login, "password": self.password, "token": 'token'}).encode('utf-8')
        response = requests.post("http://127.0.0.1:8000/auth", data=data)
        response_json = response.json()
        self.token = response_json.get("token")
        self.text = "привет!"
        self.key = [4, 2, 3]
        data = json.dumps({"text": self.text, "key": self.key, "token": self.token}).encode('utf-8')
        try:
            response = requests.post("http://127.0.0.1:8000/cipher_encrypt", data=data)
        except requests.exceptions.RequestException as e:
            self.fail(f"Ошибка при отправке запроса: {e}")
        print("\nЗашифрованный текст:", response.json().get("message"))

class Test4(unittest.TestCase):
    def test_decrypt_text(self):
        self.login = "User2"
        self.password = "Password12345.."
        data = json.dumps({"login": self.login, "password": self.password, "token": 'token'}).encode('utf-8')
        response = requests.post("http://127.0.0.1:8000/auth", data=data)
        response_json = response.json()
        self.token = response_json.get("token")
        self.text = "Ртлгжх, нбм ежоб?"
        self.key = [1, 2, 3]
        data = json.dumps({"text": self.text, "key": self.key, "token": self.token}).encode('utf-8')
        try:
            response = requests.post("http://127.0.0.1:8000/cipher_decrypt", data=data)
        except requests.exceptions.RequestException as e:
            self.fail(f"Ошибка при отправке запроса: {e}")
        print("\nРашсифрованный текст:", response.json().get("message"))

class Test5(unittest.TestCase):
    def test_change_password(self):
        self.login = "User2"
        self.password = "Password12345.."
        data = json.dumps({"login": self.login, "password": self.password, "token": 'token'}).encode('utf-8')
        response = requests.post("http://127.0.0.1:8000/auth", data=data)
        response_json = response.json()
        self.token = response_json.get("token")
        self.password1 = "testpassword735\."
        data = json.dumps({"old_password": self.password, "new_password": self.password1, "token": self.token}).encode('utf-8')
        try:
            response = requests.patch("http://127.0.0.1:8000/change_password", data=data)
        except requests.exceptions.RequestException as e:
            self.fail(f"Ошибка при отправке запроса: {e}")
        print()
        print(response.json().get("message"))


if __name__ == "__main__":
    unittest.main()

