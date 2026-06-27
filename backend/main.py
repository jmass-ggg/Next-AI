from http.server import BaseHTTPRequestHandler,HTTPServer
from services.auth import AuthServices
from api.auth import AuthApi

auth=AuthServices()

class MainHandler(BaseHTTPRequestHandler):
    def parse(self):
        return self.path.strip("/").split("/")
    
    def do_POST(self):
        path=self.parse()
        if path[0] == "auth":
            if path[1] == "register":
                AuthApi(self,auth).register()
            elif path[1] == "login":
                AuthApi(self,auth).login()
                
def run():
    server=HTTPServer(("localhost",8000),MainHandler)
    print("server running ")
    server.serve_forever()
    
if __name__ == "__main__":
    run()