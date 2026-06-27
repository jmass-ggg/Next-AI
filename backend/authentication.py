import jwt
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

def create_access_token(email):
    payload={
        "sub":str(email),
        "token_type":"access",
        "exp":datetime.utcnow() + timedelta(seconds=900)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

def create_refresh_token(email):
    payload={
        "sub":str(email),
        "token_type":"refresh",
        "exp":datetime.utcnow() + timedelta(seconds=604800)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

def verify_access_token(token):
    payload=jwt.decode(
        token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    if payload.get("access") != "access":
        return "Invalid access token type"
    email=payload.get("sub")
    if not email:
        return "Invalid token payload"
    return email
     
            
def verify_refresh_token(token):
    payload=jwt.decode(
        token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    if payload.get("access") != "refresh":
        return "Invalid access token type"
    email=payload.get("sub")
    if not email:
        return "Invalid token payload"
    return email





