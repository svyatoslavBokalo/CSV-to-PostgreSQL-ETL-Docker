from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os


class PostgresDB:
    def __init__(self, dbname, user, password,  host=os.getenv('DB_HOST', 'localhost'), port='5432'):
        """
        Ініціалізує об'єкт для підключення до бази даних PostgreSQL.

        :param dbname: Ім'я бази даних
        :param user: Ім'я користувача для підключення
        :param password: Пароль користувача
        :param host: Хост бази даних (за замовчуванням 'localhost')
        :param port: Порт бази даних (за замовчуванням '5432')
        """
        self.connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        self.engine = None
        self.session = None

    def connect(self):
        """Створює підключення до бази даних і встановлює сесію."""
        try:
            self.engine = create_engine(self.connection_string)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            print("Підключення до бази даних успішно створено.")
        except Exception as e:
            print(f"Помилка підключення до бази даних: {e}")
            self.engine = None
            self.session = None

    def execute_query(self, query):
        """
        Виконує SQL-запит до бази даних.

        :param query: SQL-запит у вигляді рядка
        :return: Результати запиту у вигляді списку рядків або None, якщо запит не повертає результат
        """
        if self.session:
            try:
                result = self.session.execute(query)
                self.session.commit()
                print("Запит успішно виконано.")
                return result.fetchall()  # Повертає всі результати у вигляді списку рядків
            except Exception as e:
                print(f"Помилка під час виконання запиту: {e}")
                self.session.rollback()
                return None
        else:
            print("Сесія не встановлена. Підключіться до бази даних перед виконанням запиту.")
            return None

    def insert_user(self, user_id, name, email, signup_date, domain):
        """Вставляє дані користувача у таблицю 'users'."""
        if self.session is not None:
            try:
                query = text("""
                        INSERT INTO users (user_id, name, email, signup_date, domain)
                        VALUES (:user_id, :name, :email, :signup_date, :domain)
                        ON CONFLICT (user_id) DO UPDATE SET
                            name = EXCLUDED.name,
                            email = EXCLUDED.email,
                            signup_date = EXCLUDED.signup_date,
                            domain = EXCLUDED.domain;
                    """)
                self.session.execute(query, {
                    'user_id': user_id,
                    'name': name,
                    'email': email,
                    'signup_date': signup_date,
                    'domain': domain
                })
                self.session.commit()
            except Exception as e:
                print(f"Помилка під час вставки даних: {e}")
                self.session.rollback()
        else:
            print("Сесія не встановлена. Підключіться до бази даних перед вставкою даних.")

    def insert_all_users_from_dataframe(df, db):
        """
        Вставляє всі дані з DataFrame у таблицю бази даних, використовуючи метод insert_user.

        :param df: DataFrame з даними
        :param db: Об'єкт класу PostgresDB, підключений до бази даних
        """
        try:
            for index, row in df.iterrows():
                db.insert_user(
                    user_id=row['user_id'],
                    name=row['name'],
                    email=row['email'],
                    signup_date=row['signup_date'],
                    domain=row['domain']
                )
            print("Всі дані з DataFrame успішно додані до бази даних.")
        except Exception as e:
            print(f"Помилка під час додавання даних до бази даних: {e}")

    def create_users_table(self):
        create_table_query = text("""
            CREATE TABLE IF NOT EXISTS users (
                user_id UUID PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                signup_date DATE NOT NULL,
                domain VARCHAR(255) NOT NULL
            );
        """)
        self.session.execute(create_table_query)
        self.session.commit()

    def close(self):
        """Закриває підключення до бази даних."""
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
        print("Підключення до бази даних закрито.")