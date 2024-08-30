import data_processor_PANDAS
import DbContext
import queries

def print_hi(name):
    #input_path = 'csvFiles/generated_users.csv'
    #output_path = 'csvFiles/processed_users.csv'

    #df = data_processor.read_csv_file(input_path)
    #df = data_processor.process_data(df)
    #data_processor.save_to_csv(df, output_path)

    # Ініціалізуємо об'єкт бази даних
    db = DbContext.PostgresDB(dbname='ETL', user='postgres', password='anafema942')
    db.connect()

    # Вказуємо шлях до CSV-файлу та назву таблиці в базі даних
    #csv_file_path = 'csvFiles/processed_users.csv'
    table_name = 'users'

    # Викликаємо функцію для додавання даних до бази даних
    #data_processor_PANDAS.insert_csv_to_db(csv_file_path, table_name, db)
    print(db.execute_query(queries.query5))
    # Закриваємо підключення до бази даних
    db.close()
    #////////////////////////////////////////////////////////////////////////////////
    #input_path = 'csvFiles/generated_users.csv'
    #output_path = 'csvFiles/processed_users_pySpark.csv'

    #df = Data_processor_PySpark.read_csv_file(input_path)
    #df = Data_processor_PySpark.process_data(df)
    #Data_processor_PySpark.save_to_csv(df, output_path)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/