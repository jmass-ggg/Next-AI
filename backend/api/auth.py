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

            self.req.send_header(
                "Set-Cookie",
                f"refresh_token={data['refresh_token']}; HttpOnly; Path=/; Max-Age=604800"
            )

           
            del data["access_token"]
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
        
    def profile(self):
        token=self.auth.get_cookie("access_token")
        if not token:
            self.response({"error": "Login required"})
            return
        email=verify_access_token(token)
        data=self.service.profile(email)
        return data
    def refresh_token(self):
        refresh_token=self.get_cookie("refresh_token")
        if not self.refresh_token:
            self.response({"error": "No refresh token"})
            return
        email=verify_refresh_token(email)
        access_token=create_access_token(email)
        return {
            "successfully":True,
            "access_token":access_token
        }
        