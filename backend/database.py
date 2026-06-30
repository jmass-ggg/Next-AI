import psycopg2

class Database:
    def __init__(self,db_name="next.db"):
        self.db_name=db_name
        self.init_db()
    
    def connect(self):
        return psycopg2.connect(
            host="localhost",
            port=5432,
            database="NextAI",
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
            """
            CREATE TABLE IF NOT EXISTS users(
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                username VARCHAR(50) NOT NULL,
                email VARCHAR(50) UNIQUE NOT NULL,
                PASSWORD VARCHAR(200) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS student_profiles (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID NOT NULL ,
            full_name VARCHAR(150),
            age INT,
            phone_number VARCHAR(20),
            bio TEXT,
            github_url VARCHAR(255),
            linkedin_url VARCHAR(255),
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
            """ 
        )
        conn.commit()
        conn.close()
        
        