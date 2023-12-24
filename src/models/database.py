# import os
# import mysql.connector


# from dotenv import load_dotenv

# from src.helpers.logger_config import CustomLogger

# load_dotenv()

# logger = CustomLogger(__name__)


# class DBConnection:
#     """This class helps to make a connection to a database"""

#     def __init__(self):
#         self.mydb = mysql.connector.connect(
#             host=os.getenv("DB_HOST"),
#             user=os.getenv("USER"),
#             passwd=os.getenv("DB_PASSWORD"),
#             database=os.getenv("DB_NAME"),
#         )
#         self.cursor = self.mydb.cursor()

#     def get_cursor(self):
#         logger.debug("Getting database cursor")
#         return self.cursor

#     def get_database_connection(self):
#         logger.debug("Getting database connection")
#         return self.mydb


# db = DBConnection()
# db_cursor = db.get_cursor()
# db_connection = db.get_database_connection()


# def get_item(query, data):
#     """get item from database

#     Args:
#         query (sql query): query to get item from database
#         data (tuple): replace query placeholder with tuple values

#     Returns:
#         tuple: return a tuple of data
#     """
#     try:
#         logger.debug(f"Executing get_item query: {query}")
#         db_cursor.execute(query, data)
#         response = db_cursor.fetchone()
#         db_connection.commit()
#         logger.debug("get_item query executed successfully")
#         return response
#     except mysql.connector.Error as error:
#         logger.error(f"Error occurred while executing get_item query: {error}")


# def get_items(query, data):
#     """get items from database

#     Args:
#         query (sql query): query to get item from database
#         data (tuple): replace query placeholder with tuple values

#     Returns:
#         tuple: return a tuple of data
#     """
#     try:
#         logger.debug(f"Executing get_items query: {query}")
#         db_cursor.execute(query, data)
#         response = db_cursor.fetchall()
#         db_connection.commit()
#         logger.debug("get_items query executed successfully")
#         return response
#     except mysql.connector.Error as error:
#         logger.error(f"Error occurred while executing get_items query: {error}")


# def insert_item(query, data):
#     """insert item into databases

#     Args:
#         query (sql query): query to update item from database
#         data (tuple): replace query placeholder with tuple values

#     """
#     try:
#         logger.debug(f"Executing insert_item query: {query}")
#         db_cursor.execute(query, data)
#         db_connection.commit()
#         logger.debug("insert_item query executed successfully")
#     except mysql.connector.Error as error:
#         logger.error(f"Error occurred while executing insert_item query: {error}")


# def update_item(query, data):
#     """update item into databases

#     Args:
#         query (sql query): query to update item from database
#         data (tuple): replace query placeholder with tuple values
#     """
#     try:
#         logger.debug(f"Executing update_item query: {query}")
#         db_cursor.execute(query, data)
#         db_connection.commit()
#         logger.debug("update_item query executed successfully")
#     except mysql.connector.Error as error:
#         logger.error(f"Error occurred while executing update_item query: {error}")


# adding other code
import os
import mysql.connector

from dotenv import load_dotenv

from src.helpers.logger_config import CustomLogger

load_dotenv()

logger = CustomLogger(__name__)


class DBConnection:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("USER"),
            passwd=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        self.cursor = self.mydb.cursor(buffered=True)

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mydb.commit()
        self.mydb.close()


def get_item(query, data):
    with DBConnection() as cursor:
        try:
            logger.debug(f"Executing get_item query: {query}")
            cursor.execute(query, data)
            response = cursor.fetchone()
            logger.debug("get_item query executed successfully")
            return response
        except mysql.connector.Error as error:
            logger.error(f"Error occurred while executing get_item query: {error}")


def get_items(query, data):
    with DBConnection() as cursor:
        try:
            logger.debug(f"Executing get_items query: {query}")
            cursor.execute(query, data)
            response = cursor.fetchall()
            logger.debug("get_items query executed successfully")
            return response
        except mysql.connector.Error as error:
            logger.error(f"Error occurred while executing get_items query: {error}")


def insert_item(query, data):
    with DBConnection() as cursor:
        try:
            logger.debug(f"Executing insert_item query: {query}")
            cursor.execute(query, data)
            logger.debug("insert_item query executed successfully")
        except mysql.connector.Error as error:
            logger.error(f"Error occurred while executing insert_item query: {error}")


def update_item(query, data):
    with DBConnection() as cursor:
        try:
            logger.debug(f"Executing update_item query: {query}")
            cursor.execute(query, data)
            logger.debug("update_item query executed successfully")
        except mysql.connector.Error as error:
            logger.error(f"Error occurred while executing update_item query: {error}")
