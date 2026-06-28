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
    
    def response(self,data):
        self.req.send_response(200)
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
    
    def login(self):
        data=self.read()
        self.response(self.service.login(data["email"],data["password"]))
        
    def profiles(self):
        access_token=self.get_cookie("access_token")
        email=verify_access_token(access_token)
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
        
    
