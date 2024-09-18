import logging
import re

import pandas as pd
from email_validator import validate_email, EmailNotValidError

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_csv_file(file_path):
    """Reading data from a CSV file"""
    df = pd.read_csv(file_path, delimiter=';')
    return df

def format_signup_date(df):
    """
    Converts the signup_date field to the standard format (YYYY-MM-DD).

    :param df: DataFrame with data
    :return: DataFrame with formatted date
    """
    df['signup_date'] = pd.to_datetime(
        df['signup_date'],
        format='%d.%m.%Y %H:%M',
        dayfirst=True,
        errors='coerce'
    ).dt.strftime('%Y-%m-%d')
    return df

def filter_invalid_emails(df):
    """
    Filters records where the email field does not contain a valid email address.

    :param df: DataFrame with data
    :return: DataFrame with valid email addresses
    """
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    df = df[df['email'].apply(lambda x: re.match(email_pattern, x) is not None)]
    return df


def filter_invalid_emails_validator(df):
    """
    Filters records where the email field does not contain a valid email address using the email-validator library.

    :param df: DataFrame with data
    :return: DataFrame with valid email addresses
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
    Adds a new domain column that contains the domain name from the email address.

    :param df: DataFrame with data
    :return: DataFrame with added domain column
    """
    df = df.copy()
    df.loc[:, 'domain'] = df['email'].apply(lambda x: x.split('@')[1])
    return df

def process_data(df):
    """
        Processes data: date formatting, filtering invalid emails, adding a domain.

        :param df: DataFrame with data
        :return: Processed DataFrame
        """
    # Converting the signup_date field to YYYY-MM-DD format
    df = format_signup_date(df)

    # Filtering invalid email addresses
    df = filter_invalid_emails_validator(df)

    # Add a domain column
    df = add_email_domain(df)

    # Return the processed DataFrame
    return df

def save_to_csv(df, output_file_path):
    """
    Saves the processed data to a new CSV file.

    :param df: DataFrame with processed data
    :param output_file_path: Source CSV file path
    """
    df.to_csv(output_file_path, index=False, sep=';', quoting=1)
    logging.info(f"The file was successfully saved to: {output_file_path}")


def insert_csv_to_db(csv_file_path, table_name, db):
    """
    Reads data from a CSV file and adds it to a table in the PostgreSQL database.

    :param csv_file_path: CSV file path
    :param table_name: Table name in database
    :param db: PostgresDB class object that is connected to the database
    """
    try:
        # Read data from CSV file in DataFrame
        df = pd.read_csv(csv_file_path, sep=';')

        # Add data to the table in the database
        df.to_sql(table_name, db.engine, if_exists='append', index=False)

        logging.info(f"Data was successfully added to the '{table_name}' table in the database.")
    except Exception as e:
        logging.error(f"Error adding data to database: {e}")






