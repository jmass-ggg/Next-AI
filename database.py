import psycopg2

class Database:
    def __init__(self,db_name="next.db"):
        self.db_name=db_name
        self.init_db()
        
    def connect(self):
        return psycopg2.connect(
            host="localhost",
            port=5432,
            database="NextAi",
            user="postgres",
            password="Kanye@12"
        )
    def init_db(self):
        conn=self.connect()
        cursor=conn.cursor()
        cursor.execute(
            'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
        )
        cursor.execute(
            """"
            CREATE TABLE users (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                username VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('student', 'admin') DEFAULT 'student',
                status ENUM('active', 'blocked') DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        