from pydantic import BaseModel
from typing import Union, List

class User(BaseModel): #модель для пользователя
    login: str
    password: str
    token: str
    id: Union[int, None] = None

class Change_Text_Request(BaseModel): #модель для изменения текста
    token: str
    text_number: int
    new_text: str

class Delete_Request(BaseModel): #модель для удаления текста
    token: str
    text_number: int
    type: str

class One_Text_Request(BaseModel): #модель для просмотра одного текста
    token: str
    text_number: int
    type: str

class Cipher_Request(BaseModel): #модель для шифрования, дешифрования
    text: str
    key: List[int]
    token: str

class Change_Password_Request(BaseModel): #модель для смены пароля
    old_password: str
    new_password: str
    token: str

class Text_Request(BaseModel): #модель для работы с текстом
    text: str
    token: str

class Token(BaseModel):
    token:str