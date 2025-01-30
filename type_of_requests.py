import urllib.request
import json

def send_post(url, data):
    request = urllib.request.Request(url, data=data, method='POST')
    request.add_header('Content-Type', 'application/json')
    try:
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_message = e.read().decode()
        try:
            error_data = json.loads(error_message)
            return {"error": error_data.get("detail", "Ошибка запроса")}
        except json.JSONDecodeError:
            return {"error": "Ошибка при обработке ответа сервера"}

def send_get(url, data):
    request = urllib.request.Request(url, data=data, method='GET')
    request.add_header('Content-Type', 'application/json')
    try:
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_message = e.read().decode()
        try:
            error_data = json.loads(error_message)
            return {"error": error_data.get("detail", "Ошибка запроса")}
        except json.JSONDecodeError:
            return {"error": "Ошибка при обработке ответа сервера"}

def send_patch(url, data):
    request = urllib.request.Request(url, data=data, method='PATCH')
    request.add_header('Content-Type', 'application/json')
    try:
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_message = e.read().decode()
        try:
            error_data = json.loads(error_message)
            return {"error": error_data.get("detail", "Ошибка запроса")}
        except json.JSONDecodeError:
            return {"error": "Ошибка при обработке ответа сервера"}

def send_delete(url, data):
    request = urllib.request.Request(url, data=data, method='DELETE')
    request.add_header('Content-Type', 'application/json')
    try:
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_message = e.read().decode()
        try:
            error_data = json.loads(error_message)
            return {"error": error_data.get("detail", "Ошибка запроса")}
        except json.JSONDecodeError:
            return {"error": "Ошибка при обработке ответа сервера"}