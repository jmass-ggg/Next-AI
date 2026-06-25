import hashlib
from database import Database

class AuthServices:
    def __init__(self):
        self.db=Database()
        
    def hash_password(self,password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create(self,username,email,password):
        conn=self.db.connect()
        cursor=conn.cursor()
        password_hash=self.hash_password(password)
        cursor.execute(
            """
            INSERT INTO users(username,email,password_hash)
            VALUES (%s,%s,%s)
            """,(username,email,password_hash)
            
        )
        conn.commit()
        conn.close()
        return {
            "username":username,
            "email":email
        }
        
    