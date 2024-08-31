import pandas as pd
import re
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import create_engine


def read_csv_file(file_path):
    # Читання даних з CSV-файлу
    df = pd.read_csv(file_path, delimiter=';')

    return df

def format_signup_date(df):
    """
    Переводить поле signup_date у стандартний формат (YYYY-MM-DD).

    :param df: DataFrame з даними
    :return: DataFrame з відформатованою датою
    """
    df['signup_date'] = pd.to_datetime(df['signup_date'], format='%d.%m.%Y %H:%M', dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')
    return df

def filter_invalid_emails(df):
    """
    Відфільтровує записи, де поле email не містить дійсної email-адреси.

    :param df: DataFrame з даними
    :return: DataFrame з дійсними email-адресами
    """
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    df = df[df['email'].apply(lambda x: re.match(email_pattern, x) is not None)]
    return df


def filter_invalid_emails_validator(df):
    """
    Відфільтровує записи, де поле email не містить дійсної email-адреси, використовуючи бібліотеку email-validator.

    :param df: DataFrame з даними
    :return: DataFrame з дійсними email-адресами
    """

    def is_valid_email(email):
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False

    df = df[df['email'].apply(is_valid_email)]
    return df

def add_email_domain(df):
    """
    Додає нову колонку domain, яка містить доменне ім’я з email-адреси.

    :param df: DataFrame з даними
    :return: DataFrame з доданою колонкою domain
    """
    df = df.copy()
    df.loc[:, 'domain'] = df['email'].apply(lambda x: x.split('@')[1])
    return df

def process_data(df):
    # Переведення поля signup_date у формат YYYY-MM-DD
    df = format_signup_date(df)

    # Фільтрація недійсних email-адрес
    df = filter_invalid_emails_validator(df)

    # Додавання колонки domain
    df = add_email_domain(df)

    # Повертаємо оброблений DataFrame
    return df

def save_to_csv(df, output_file_path):
    """
    Зберігає оброблені дані у новий CSV-файл.

    :param df: DataFrame з обробленими даними
    :param output_file_path: Шлях до вихідного CSV-файлу
    """
    df.to_csv(output_file_path, index=False, sep=';', quoting=1)
    print(f"Файл успішно збережено за адресою: {output_file_path}")


def insert_csv_to_db(csv_file_path, table_name, db):
    """
    Зчитує дані з CSV-файлу і додає їх до таблиці в базі даних PostgreSQL.

    :param csv_file_path: Шлях до CSV-файлу
    :param table_name: Назва таблиці в базі даних
    :param db: Об'єкт класу PostgresDB, який підключений до бази даних
    """
    try:
        # Зчитуємо дані з CSV-файлу в DataFrame
        df = pd.read_csv(csv_file_path, sep=';')

        # Додаємо дані до таблиці в базі даних
        df.to_sql(table_name, db.engine, if_exists='append', index=False)

        print(f"Дані успішно додані до таблиці '{table_name}' в базі даних.")
    except Exception as e:
        print(f"Помилка під час додавання даних до бази даних: {e}")






