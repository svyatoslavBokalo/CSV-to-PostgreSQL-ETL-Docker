from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class PostgresDB:
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
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
        :return: Результати запиту, якщо вони є
        """
        if self.session:
            try:
                result = self.session.execute(query)
                self.session.commit()
                print("Запит успішно виконано.")
                return result.fetchall()
            except Exception as e:
                print(f"Помилка під час виконання запиту: {e}")
                self.session.rollback()
                return None
        else:
            print("Сесія не встановлена. Підключіться до бази даних перед виконанням запиту.")
            return None

    def close(self):
        """Закриває підключення до бази даних."""
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
        print("Підключення до бази даних закрито.")