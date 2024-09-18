import logging
import data_processor_PANDAS
import db_context
import queries

from sqlalchemy import text

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function to process data and interact with the database.
    """
    input_path = 'csvFiles/generated_users.csv'
    output_path = 'csvFiles/processed_users.csv'

    # Read and process data
    df = data_processor_PANDAS.read_csv_file(input_path)
    df = data_processor_PANDAS.process_data(df)
    data_processor_PANDAS.save_to_csv(df, output_path)

    # Initialize the database object
    db = db_context.PostgresDB(dbname='ETL', user='postgres', password='123456789')
    db.connect()

    # Create table
    db_context.PostgresDB.create_users_table()

    # Insert data into the database
    db_context.PostgresDB.insert_all_users_from_dataframe(df, db)

    # Execute queries
    for i, query in enumerate([queries.query1, queries.query2, queries.query3, queries.query4, queries.query5], start=1):
        logger.info(f"Executing query {i}:")
        result = db.execute_query(query)
        if result is not None:
            logger.info(f"Result of query {i}: {result}")
        else:
            logger.info(f"No results returned for query {i}.")

    logger.info("An exception may occur here because the delete query does not return data. To verify, do the following:")
    logger.info("Retrieving data after deleting users except those with certain domains:")
    remaining_users = db.execute_query(text("SELECT * FROM users"))
    logger.info(f"Remaining users: {remaining_users}")

    # Close the database connection
    db.close()

if __name__ == '__main__':
    main()