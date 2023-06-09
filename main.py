"""
Нужно скачать fastapi, websockets, uvicorn:

pip install fastapi
pip install websockets
pip install uvicorn
pip install pytest-asyncio
pip install pytest

Для запуска сервера впишите в терминал: uvicorn main:app --reload
и перейдите по ссылке: http://127.0.0.1:8000

"""
from typing import Union
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import requests
import asyncio
import json

# Создаем наше FastAPI приложение
app = FastAPI()
# Кэш запросов
cache = {}

# HTML код главной страницы
html = """ 
<!DOCTYPE html>
<html>
    <head>
        <title>Factorial calculator</title>
    </head>
    <body>
        <h1>Factorial calculator</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Calculate</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) { 
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


# Функция, которая выполняется при запуске сервера
@app.on_event("startup")
async def app_startup():
    global cache
    with open("cache.txt", mode="r+") as file:
        json_data = file.read()
        if json_data:
            cache = json.loads(json_data)


# Функция, которая выполняется при закрытии сервера
@app.on_event("shutdown")
async def shutdown_event():
    global cache
    # Сохраняем запросы
    with open("cache.txt", mode="r+") as file:
        loaded_data = None
        if cache:
            loaded_data = json.dumps(cache)
        file.write(loaded_data)


# Функция вычисления факториала числа
async def calculate_factorial(number: int) -> int:
    if number == 0 or number == 1:
        return 1
    else:
        result = 1
        for i in range(2, number + 1):
            result *= i
            await asyncio.sleep(0)
        return result


# Очистить кэш
def clear_cache():
    global cache
    cache = {}


# Возращает главную страницу
@app.get("/")
async def get():
    return HTMLResponse(html)


@app.get("/greetings")
async def greet():
    return {"Timur": 'Hello, I am aiming to become a great Junior Python Developer'}


# Страница, где показан кэш
@app.get("/cache")
async def get_cache():
    global cache
    return cache


# Создаем websocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global cache

    # Встроенная функция отправления результа вычисления
    async def send_factorial_result(number: str):
        result = await calculate_factorial(int(number))
        cache[data] = result
        await websocket.send_text(f"Factorial {number}! = {str(result)}")

    # Ждем отправки сообщений
    await websocket.accept()
    # Ждем получения сообщений
    while True:

        data = await websocket.receive_text()
        # Если запрос мы уже обрабатывали, то просто выводим его, иначе создаем task рассчета факториала
        if cache.get(data):
            print(f'Getting factorial of {data} from cache')
            await websocket.send_text(f"Factorial {data}! = {str(cache[data])}")
        else:
            print(f'Calculating factorial of {data}')
            task = asyncio.create_task(send_factorial_result(data))
