import mysql.connector
from mysql.connector import Error, pooling
import streamlit as st
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

connection_pool = None

def initialize_connection_pool():
    global connection_pool  # Ensure that we modify the global connection_pool
    if connection_pool is None:
        try:
            connection_pool = pooling.MySQLConnectionPool(
                pool_name="db_pool",
                pool_size=10,  # Number of connections in the pool
                host="<host name>",
                user="<user name>",
                password="<your passwd>",
                database="<db name>
            )
            logging.info("Database connection pool created successfully.")
        except Error as e:
            logging.error(f"Error creating connection pool: {e}")
            st.error(f"Failed to connect to the database: {e}")

# Call initialize_connection_pool() at the start
initialize_connection_pool()

def get_connection():
    """Establish and return a connection from the pool."""
    try:
        conn = connection_pool.get_connection()
        if conn.is_connected():
            return conn
        else:
            logging.error("Connection pool returned a disconnected connection.")
            return None
    except Error as e:
        logging.error(f"Error getting connection from pool: {e}")
        return None

def execute_procedure(proc_name, args):
    """
    Executes a stored procedure with the given name and arguments.

    Args:
        proc_name (str): The name of the stored procedure.
        args (tuple): The arguments to pass to the procedure.

    Returns:
        result (list): A list of result sets if the procedure produces them.
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.callproc(proc_name, args)
            
            # Fetch any result sets returned by the procedure
            result = []
            for res in cursor.stored_results():
                result.append(res.fetchall())
            
            conn.commit()
            return result
        except Error as e:
            logging.error(f"Error executing procedure {proc_name}: {e}")
            raise  # Raise the error so it can be handled by the calling function
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        raise ConnectionError("Failed to establish a database connection.")

def execute_query(query, params=None):
    """Executes a query with optional parameters."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())  # Use an empty tuple if no params
            conn.commit()
        except Error as e:
            logging.error(f"Error executing query: {e}")
            st.error(f"An error occurred while executing the query: {e}")
        finally:
            cursor.close()
            conn.close()

def fetch_data(query, params=None):
    """Fetches data from the database for a given query with optional parameters."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)  # Ensure it's returning dictionaries
            cursor.execute(query, params or ())  # Use an empty tuple if no params
            result = cursor.fetchall()
            return result
        except Error as e:
            logging.error(f"Error fetching data: {e}")
            st.error(f"An error occurred while fetching data: {e}")
            return []
        finally:
            # Ensure both cursor and connection are closed
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    else:
        st.error("Database connection not available. Please try again later.")
        return []


def get_teams():
    """Fetches available teams from the database."""
    query = "SELECT Team_ID, Team_Name FROM Team;"
    return fetch_data(query)

