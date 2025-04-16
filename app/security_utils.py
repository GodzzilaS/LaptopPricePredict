import re
from typing import Any

import pandas as pd
from cryptography.fernet import Fernet

from app.config import FERNET_KEY

# Сюда добавили обработку пробелов ещё через Regex
DANGEROUS_PATTERN = re.compile(r'^\s*([=+\-@])')


def check_csv_injection(cell: Any) -> bool:
    """
    Проверяет строковое значение на наличие опасных символов,
    учитывая пробелы перед ними.
    Возвращает True, если обнаружена потенциальная CSV-инъекция.
    """
    if isinstance(cell, str) and DANGEROUS_PATTERN.match(cell):
        return True
    return False


def check_sql_injection(cell: Any) -> bool:
    """
    Проверяет строковое значение на наличие паттерна SQL-комментариев (--).
    Возвращает True, если обнаружена потенциальная SQL-инъекция.
    """
    if isinstance(cell, str) and '--' in cell:
        return True
    return False


def sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Проходит по всем строковым столбцам датафрейма и выполняет проверки
    на потенциальные CSV- и SQL-инъекции. Если обнаруживается неподходящее значение,
    выбрасывается ValueError.
    """
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

        def sanitize_value(val):
            if isinstance(val, str):
                if check_csv_injection(val):
                    raise ValueError(f"Обнаружена CSV-инъекция в столбце {col}: {val}")
                if check_sql_injection(val):
                    raise ValueError(f"Обнаружена SQL-инъекция в столбце {col}: {val}")
            return val

        df[col] = df[col].apply(sanitize_value)
    return df


fernet = Fernet(FERNET_KEY)


def encrypt_ram(df: pd.DataFrame, ram_column: str = "RAM_Size", new_column: str = "RAM_encrypted") -> pd.DataFrame:
    """
    Создает новый столбец с зашифрованными значениями из столбца ram_column.
    Если значение не строковое, приводим его к строке перед шифрованием.
    """
    if ram_column in df.columns:
        df[new_column] = df[ram_column].apply(lambda x: fernet.encrypt(str(x).encode()).decode())
    return df


def decrypt_ram_values(encrypted_values: list[str]) -> list[str]:
    """
    Принимает список зашифрованных строковых значений и возвращает список их расшифрованных значений.
    При ошибке расшифровки вставляет строку с сообщением об ошибке.
    """
    decrypted = []
    for value in encrypted_values:
        try:
            decrypted.append(fernet.decrypt(value.encode()).decode())
        except Exception:
            decrypted.append("Ошибка расшифровки")
    return decrypted


def print_first_five_decrypted_ram(df: pd.DataFrame, encrypted_column: str = "RAM_encrypted") -> None:
    """
    Выводит первые 5 расшифрованных значений из столбца с зашифрованной RAM.
    """
    if encrypted_column in df.columns:
        sample_values = df[encrypted_column].dropna().head(5).tolist()
        decrypted = decrypt_ram_values(sample_values)
        print("Первые 5 расшифрованных значений RAM:")
        for val in decrypted:
            print(val)
