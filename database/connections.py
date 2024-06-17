import mysql.connector
from mysql.connector import errorcode
from database.settings import *
from fastapi import HTTPException


db_config = {
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "host": MYSQL_HOST,
    "database": MYSQL_DB,
    "raise_on_warnings": True,
}


# Connect to MySQL database
# def connect():
#     return mysql.connector.connect(
#         user=MYSQL_USER,
#         host=MYSQL_HOST,
#         password=MYSQL_PASSWORD,
#         database=MYSQL_DB
#     )


def connect():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise HTTPException(
                status_code=500, detail="Error: Access denied. Check your credentials."
            )
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise HTTPException(
                status_code=500, detail="Error: The specified database does not exist."
            )
        else:
            raise HTTPException(status_code=500, detail=f"Error: {err}")
        raise
