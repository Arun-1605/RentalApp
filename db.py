



import pymysql
from config import Config

# Function to connect to the database
def get_db_connection():
    connection = pymysql.connect(
        charset="utf8mb4",
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        db=Config.DB_NAME,
        port=Config.DB_PORT,
        cursorclass=pymysql.cursors.DictCursor,
    )
    return connection
