import threading
import time
from pprint import pprint

import requests
import uvicorn


def send_test_request():
    time.sleep(3)  # Увеличиваем время ожидания

    try:
        with open('data/Laptop_price.csv', 'rb') as f:
            print("\nSending test request...")
            response = requests.post(
                "http://localhost:8000/predict/",
                files={'file': f},
                timeout=10
            )

            print("\n=== Test Request Results ===")
            if response.status_code == 200:
                pprint(response.json(), indent=2)
            else:
                print(f"Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"\nRequest failed: {str(e)}")


def run_server():
    # Убираем reload и выносим конфигурацию
    config = uvicorn.Config(
        "app.api:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=False  # Отключаем перезагрузку
    )

    # Запускаем сервер в основном потоке
    server = uvicorn.Server(config)
    server_thread = threading.Thread(target=server.run)
    server_thread.daemon = True
    server_thread.start()

    send_test_request()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")


if __name__ == "__main__":
    print("Starting API server with auto-test...")
    run_server()
