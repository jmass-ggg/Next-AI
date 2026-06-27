import hashlib
from database import Database
from authentication import create_access_token,create_refresh_token
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
            INSERT INTO users(username,email,password)
            VALUES (%s,%s,%s)
            """,(username,email,password_hash)
            
        )
        
        conn.commit()
        conn.close()
        return {
            "username":username,
            "email":email
        }
    def login(self,email,password):
        conn=self.db.connect()
        cursor=conn.cursor()
        pwd_hash=self.hash_password(password)
        cursor.execute(
           """
            SELECT id,email, password
            FROM users
            WHERE email = %s AND password = %s
            """,
            (email,pwd_hash)
            
        )
        
        user=cursor.fetchone()
        print(user)
        if user:
            access=create_access_token(email)
            refresh=create_refresh_token(email)
            
            return {
                "login":'successfully',
                "access_token":access
            }
        conn.close()
        cursor.close()
        return {
            "error":"Invalid Credentials"  
        }