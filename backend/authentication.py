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
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("token_type") != "access":
            return None

        return payload.get("sub")

    except Exception:
        return None
     
            
def verify_refresh_token(token):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("token_type") != "refresh":
            return None

        return payload.get("sub")

    except Exception:
        return None




