import threading
import time
from pprint import pprint

import requests
import uvicorn


def send_test_request():
    time.sleep(3)

    try:
        with open('data/Laptop_price.csv', 'rb') as f:
            print("\nОтправка POST запроса...")
            response = requests.post(
                "http://localhost:8000/predict/",
                files={'file': f},
                timeout=10
            )

            print("\n=== Ответ от API ===")
            if response.status_code == 200:
                pprint(response.json(), indent=2)
            else:
                print(f"Ошибка {response.status_code}: {response.text}")

    except Exception as e:
        print(f"\nЗапрос не выполнен: {str(e)}")


def run_server():
    config = uvicorn.Config(
        "app.api:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=False
    )

    server = uvicorn.Server(config)
    server_thread = threading.Thread(target=server.run)
    server_thread.daemon = True
    server_thread.start()

    send_test_request()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nОстановка сервера...")


if __name__ == "__main__":
    print("Запуск сервера с автоматическим тестированием...")
    run_server()
