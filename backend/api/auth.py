import json
from http.cookies import SimpleCookie
from authentication import create_access_token,create_refresh_token,verify_access_token,verify_refresh_token

class AuthApi:
    def __init__(self,req,service):
        self.req = req
        self.service = service
    
    def read(self):
        length=int(self.req.headers.get("Content-Length", 0))
        body=self.req.rfile.read(length)
        return json.loads(body) if body else {}
    
    def get_cookie(self,name):
        cookies=SimpleCookie()
        cookies.load(self.req.headers.get("Cookie", ""))

        if name in cookies:
            return cookies[name].value

        return None
    
    def get_bearer_token(self):
        auth_header=self.req.headers.get("Authorization")
        if not auth_header:
            return None
        if not auth_header.startswith("Bearer "):
            return None

        return auth_header.split(" ", 1)[1]
    
    def response(self,data,status=200):
        self.req.send_response(status)
        if "access_token" in data:
            self.req.send_header(
            "Set-Cookie",
            f"access_token={data['access_token']}; HttpOnly; Path=/; Max-Age=900"
            )
            
        if "refresh_token" in data:
            self.req.send_header(
            "Set-Cookie",
            f"refresh_token={data['refresh_token']}; HttpOnly; Path=/; Max-Age=604800" 
            )
            del data["refresh_token"]   
        self.req.send_header("Content-Type", "application/json")
        self.req.end_headers()
        self.req.wfile.write(json.dumps(data).encode())
        
    def register(self):
        data=self.read()
        self.response(self.service.create(data["username"],data["email"],data["password"]))
        
    def require_auth(self):
        token = self.get_bearer_token()

        if not token:
            token = self.get_cookie("access_token")

        if not token:
            self.response({"error": "Login required"}, status=401)
            return None

        email = verify_access_token(token)

        if not email:
            self.response({"error": "Invalid or expired access token"}, status=401)
            return None

        return email
    
    def login(self):
        data=self.read()
        self.response(self.service.login(data["email"],data["password"]))
        
    def profiles(self):
        
        email=self.require_auth()
        if not email:
            self.response({"error":"User not found"})
            return
        self.response(self.service.profile(email))
    
    def new_Access_Token(self):
        refresh_token=self.get_cookie("refresh_token")
        email=verify_refresh_token(refresh_token)
        if not email:
            self.response({"error":"User not found"})
            return
        self.response(self.service.createNewAccessToken(email))
        
    def user_profiles(self):
        data = self.read()

        email = self.require_auth()

        if not email:
            return

        user_id = self.service.get_user_id(email)

        if not user_id:
            self.response({"error": "User not found"}, status=404)
            return

        result = self.service.user_profile(
            user_id=user_id,
            full_name=data["full_name"],
            age=data["age"],
            phone_number=data["phone_number"],
            bio=data["bio"],
            github_url=data["github_url"],
            linkedin_url=data["linkedin_url"]
        )

        self.response(result)
        
    
    def get_user_profile(self,user_profile_id):
        self.response(self.service.get_user_profiles(user_profile_id))
    
    def patch_user_profile(self,user_profile_id):
        data=self.read()
        self.response(self.service.patch_user_profiles(user_profile_id,data))
    
    def delete_user_profile(self,user_profile_id):
        self.response(self.service.delete_user_profile(user_profile_id))