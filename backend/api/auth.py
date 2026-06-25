import json

class AuthApi:
    def __init__(self,req,service):
        self.req = req
        self.service = service
    
    def read(self):
        length=int(self.req.headers.get("Content-Length", 0))
        body=self.req.rfile.read(length)
        return json.loads(body) if body else {}
    
    def response(self,data):
        self.req.send_response(200)
        self.req.send_header("Content-Type", "application/json")
        self.req.end_header()
        self.req.wfile.write(json.dump(data).encode())
        
    def register(self):
        data=self.read
        self.response(self.service.create(data["username"],data["email"],data["password"]))