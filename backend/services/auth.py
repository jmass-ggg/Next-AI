import hashlib
from database import Database
from authentication import create_access_token,create_refresh_token,verify_access_token,verify_refresh_token
from api.auth import AuthApi

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
  
        if user:
            access=create_access_token(email)
            refresh=create_refresh_token(email)
            
            
            return {
                "login":'successfully',
                "access_token":access,
                 "refresh_token":refresh
            }
        conn.close()
        cursor.close()
        return {
            "error":"Invalid Credentials"  
        }
    def profile(self,email):
        conn=self.db.connect()
        cursor=conn.cursor()
        cursor.execute(
            """
            SELECT id , username ,email
            FROM users
            WHERE email = %s
            """,(email,)
        )
        user=cursor.fetchone()
        if not user:
            return "User not found"
        return {
            "id":user[0],
            "username": user[1],
            "email":user[2]
        }
        
    def get_user_id(self,email):
        conn=self.db.connect()
        cursor=conn.cursor()
        cursor.execute(
            """
            SELECT id 
            FROM users
            WHERE email = %s
            """,(email,)
        )
        user=cursor.fetchone()
        if not user:
            return None
        return user[0]
    
    def createNewAccessToken(self,email):
        conn=self.db.connect()
        cursor=conn.cursor()
        cursor.execute(
            """
            SELECT email
            FROM users
            WHERE email = %s
            """,(email,)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return {"error": "User not found"}
        newAccessToken=create_access_token(user[0])
        return {
        "success": True,
        "message": "New access token created",
        "access_token": newAccessToken
         }
        
    def user_profile(self,user_id,full_name,age,phone_number,bio,github_url,linkedin_url):
        conn=self.db.connect()
        cursor=conn.cursor()
        cursor.execute(
            """
            INSERT INTO student_profiles(user_id,full_name,age,phone_number,bio,github_url,linkedin_url)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,(user_id,full_name,age,phone_number,bio,github_url,linkedin_url)
            
        )
        cursor.close()
        conn.close()
        return {
        "success": True,
        "message": "Student profile created"
        }
    def get_user_profiles(self,user_profile_id):
        conn=self.db.connect()
        cursor=conn.cursor()
        cursor.execute(
            """
            SELECT * FROM 
            student_profiles
            WHERE id= %s
            """,(user_profile_id,)
            
        )
        user=cursor.fetchone()
        if not user:
            return {"error ":"User not found"}
        conn.close()
        cursor.close()
        return {
            "id":user[0],
            "user_id":user[1],
            "full_name":user[2],
            "age":user[3],
            "phone_number":user[4],
            "bio":user[5],
            "github_url":user[6],
            "linkedin_url":user[7]
        }
    def patch_user_profiles(self,user_profile_id,**kwargs):
        conn=self.db.connect()
        cursor=conn.cursor()
        fields=[]
        value=[]
        allow_fields=[
            "full_name","age","phone_number","bio","github_url","linkedin_url"
        ]
        for key in allow_fields:
            if key and kwargs[key] is not None:
                fields.append(f"{key} = %s")
                value.append(kwargs[key])
        value.append(user_profile_id)
        query=cursor.execute(
            
            f"""
            UPDATE student_profiles
            SET {" ,".join(fields)}
            WHERE id =%s
            RETURN id
            """
            
        )
        cursor.execute(query,value)
        student_profiles_id=cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return {
            "student_profile":student_profiles_id
        }