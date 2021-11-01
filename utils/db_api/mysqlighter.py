from mysql.connector import connect, Error, errorcode
from enum import Enum


class deleteType(Enum):
    DELETE_DATABASE = "delete_database"
    DELETE_TABLE = "delete_table"
    DELETE_RECORDS = "delete_records"


class MySQL:
    def __init__(self, host_ip, host_user, host_pass, db_name=None):
        try:
            self.connection = connect(
                host=host_ip,
                port=3306,
                user=host_user,
                password=host_pass,
                database=db_name
            )
            # print("Connection to MYSQL Successfully")
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("You have another problem")

    def execute_query(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
            # print("Query executed successfully")
        except Error as err:
            print(f"The error '{err}' occurred")

    def execute_read_query(self, query):
        result = None
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
            return result
        except Error as err:
            print(f"The error '{err}' occurred")

    def execute_create_database_query(self, db_name):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("USE {}".format(db_name))
            print("Database {} is already exists".format(db_name))
        except Error as err:
            print("Database {} does not exists.".format(db_name))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.execute_query("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
                print("Database {} created successfully.".format(db_name))
            else:
                print("Failed creating database: {}".format(err))

    def execute_create_table_database_query(self, table_name, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
            print("Creating table {} Successfully ".format(table_name))
        except Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table is already exists.")
            else:
                print(f"The error '{err}' occurred")

    def execute_delete_data_db_query(self, db_name, table_name, records, types):
        finally_message = None
        try:
            if types == deleteType.DELETE_DATABASE.value:
                delete_query = f"DROP DATABASE `{db_name}`;"
                finally_message = f"Select {types} and this database {db_name} was delete."
            elif types == deleteType.DELETE_TABLE.value:
                delete_query = f"DROP TABLE `{table_name}`;"
                finally_message = f"Select {types} and in database: {db_name} was delete table: {table_name}."
            elif types == deleteType.DELETE_RECORDS.value:
                delete_query = f"""DELETE FROM {table_name} WHERE {records};"""
                finally_message = f"Select {types} and in database: {db_name} was delete record: {records} in table: {table_name}."
            else:
                print(f"Error {types} is bad request.")
                return
            if types != "delete_database" and table_name is not None or records is not None:
                self.connection.database = db_name
            with self.connection.cursor() as cursor:
                cursor.execute(delete_query)
                self.connection.commit()
        except Error as err:
            print(f"The error '{err}' occurred")
