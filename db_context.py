import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Logging Configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler and formatter
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class PostgresDB:
    """
        Class for connecting and interacting with the PostgreSQL database.
    """
    def __init__(
        self,
        dbname: str,
        user: str,
        password: str,
        host: str = os.getenv('DB_HOST', 'localhost'),
        port: str = '5432'
    ):
        """
        Initializes the object to connect to the PostgreSQL database.

        :param dbname: database name
        :param user: User name for connection
        :param password: user password
        :param host: Database host (default is' localhost ')
        :param port: Database port (default '5432')
        """
        self.connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        self.engine = None
        self.session = None

    def connect(self):
        """Creates a database connection and establishes a session."""
        try:
            self.engine = create_engine(self.connection_string)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            logger.info("Database connection created successfully.")
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            self.engine = None
            self.session = None

    def execute_query(self, query: str):
        """
        Performs an SQL query on the database.

        :param query: SQL query as string
        :return: Query results as a list of rows or None if the query does not return a result
        """
        if self.session:
            try:
                result = self.session.execute(query)
                self.session.commit()
                logger.info("The request completed successfully.")
                return result.fetchall()  # Returns all results as a list of strings
            except Exception as e:
                logger.error(f"Error executing query: {e}")
                self.session.rollback()
                return None
        else:
            logger.warning("Session not set. Connect to the database before running the query.")
            return None

    def insert_user(self, user_id, name, email, signup_date, domain):
        """Inserts user data into the 'users' table."""
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
                logger.error(f"Error inserting data: {e}")
                self.session.rollback()
        else:
            logger.warning("Session not set. Connect to the database before inserting data.")

    def insert_all_users_from_dataframe(df, db):
        """
        Inserts all data from the DataFrame into the database table using the insert_user method.

        :param df: DataFrame with data
        :param db: PostgresDB class object connected to the database
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
            logger.info("All data from the DataFrame was successfully added to the database.")
        except Exception as e:
            logger.error(f"Error adding data to database: {e}")

    def create_users_table(self):
        """Creates a'Users' table in the database if it does not exist."""
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
        """Closes the database connection."""
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()
        logger.info("Database connection closed.")