"""
Нужно скачать fastapi, websockets, uvicorn:

pip install fastapi
pip install websockets
pip install uvicorn

Для запуска сервера впишите в терминал: uvicorn main:app --reload
и перейдите по ссылке: http://127.0.0.1:8000

"""

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio

# Создаем наше FastAPI приложение
app = FastAPI()

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


# Возращает главную страницу
@app.get("/")
async def get():
    return HTMLResponse(html)


# Создаем websocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Встроенная функция отправления результа вычисления
    async def send_factorial_result(number: str):
        result = await calculate_factorial(int(number))
        await websocket.send_text(f"Factorial {number}! = {str(result)}")

    # Ждем отправки сообщений
    await websocket.accept()
    # Ждем получения сообщений
    while True:

        data = await websocket.receive_text()
        print(f'Calculating factorial of {data}')

        try:
            task = asyncio.create_task(send_factorial_result(data))
        except:
            print('An error has occurred...')
