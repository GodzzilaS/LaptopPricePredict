## Описание проекта
Простой сервис на Python 3.13.2, предсказывающий цену ноутбука на основе входных данных. Используется ML-модель, FastAPI и pandas.

## Структура проекта
```
Laptop/
├── app/
│   ├── api.py                  # API FastAPI
│   ├── config.py               # Конфигурация проекта
│   ├── model.py                # Работа с ML-моделью
│   └── schemas.py              # Валидация данных
├── data/
│   └── Laptop_price.csv        # Датасет для обучения
├── models/
│   └── laptop_price_model.pkl  # Обученная модель
├── serve.py                    # Запуск API
├── train.py                    # Скрипт обучения модели
└── requirements.txt            # Зависимости проекта
```

## Запуск проекта

### Установка зависимостей:
```bash
pip install -r requirements.txt
```

### Обучение модели:
```bash
python train.py
```

### Запуск API:
```bash
python serve.py
```