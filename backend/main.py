from http.server import BaseHTTPRequestHandler,HTTPServer
from services.auth import AuthServices
from api.auth import AuthApi

auth=AuthServices()

class MainHandler(BaseHTTPRequestHandler):
    def parse(self):
        return self.path.strip("/").split("/")
    def do_GET(self):
        path=self.parse()
        if path[0] == "auth":
            if path[1] == "me":
                AuthApi(self,auth).profiles()
            elif path[1] == "refresh":
                AuthApi(self,auth).new_Access_Token()
        elif path[0] == "student":
            AuthApi(self,auth).get_user_profile()
            
        
    def do_POST(self):
        path=self.parse()
        if path[0] == "auth":
            if path[1] == "register":
                AuthApi(self,auth).register()
            elif path[1] == "login":
                AuthApi(self,auth).login()
            elif path[1] == "me":
                AuthApi(self,auth).profile()
        elif path[0]=="student":
            AuthApi(self,auth).user_profiles()
            
    def do_PATCH(self):
        path=self.parse()
        if path[0] == "students":
            AuthApi(self,auth).patch_user_profile()
    
    def do_DELETE(self):
        path=self.parse()
        if path[0] == "student":
            AuthApi(self,auth).delete_user_profile()
                
                
def run():
    server=HTTPServer(("localhost",8000),MainHandler)
    print("server running ")
    server.serve_forever()
    
if __name__ == "__main__":
    run()