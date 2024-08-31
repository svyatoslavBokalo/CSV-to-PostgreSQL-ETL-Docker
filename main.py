import data_processor_PANDAS
import DbContext
import queries

def print_hi(name):
    input_path = 'csvFiles/generated_users.csv'
    output_path = 'csvFiles/processed_users.csv'

    df = data_processor_PANDAS.read_csv_file(input_path)
    df = data_processor_PANDAS.process_data(df)
    data_processor_PANDAS.save_to_csv(df, output_path)

    # Ініціалізуємо об'єкт бази даних
    db = DbContext.PostgresDB(dbname='ETL', user='postgres', password='123456789')
    db.connect()

    # Вказуємо шлях до CSV-файлу та назву таблиці в базі даних
    csv_file_path = 'csvFiles/processed_users.csv'
    table_name = 'users'

    # Викликаємо функцію для додавання даних до бази даних
    #data_processor_PANDAS.insert_csv_to_db(csv_file_path, table_name, db)
    DbContext.PostgresDB.insert_all_users_from_dataframe(df, db)
    #data_processor_PANDAS.insert_dataframe_to_db_optimized(df, table_name, db)

    print("викликаємо 1 запит: ")
    print(db.execute_query(queries.query1))

    print("викликаємо 2 запит: ")
    print(db.execute_query(queries.query2))

    print("викликаємо 3 запит: ")
    print(db.execute_query(queries.query3))

    print("викликаємо 4 запит: ")
    print(db.execute_query(queries.query4))

    print("викликаємо 5 запит: ")
    print(db.execute_query(queries.query5))
    print("тут виникає виняток, який обробляє і каже, що саме цей запит (delete) немає на виході даних тому перевіряєм, ось так:")
    print("отримуємо дані, після очищення всіх користувачів окрім, які мають певні домени",db.execute_query("SELECT * FROM users"))
    print("/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
    print("видалення всіх даних з бд")
    print()
    print(db.execute_query("DELETE FROM users;"))
    print("/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")

    # Закриваємо підключення до бази даних
    db.close()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/