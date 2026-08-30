import os
from datetime import datetime, timezone, timedelta
from uuid import uuid4

import jwt

from utils.environment_util import load_env


class TokenUtil:
    @staticmethod
    def create_access_token(payload:dict)->dict:
        SECRET_KEY= os.environ.get('JWT_SECRET_KEY')
        ALGORITHM="HS256"
        token=jwt.encode(
            payload=payload,
            key=SECRET_KEY,
            algorithm=ALGORITHM,
        )
        return token

    @staticmethod
    def decode_token(token:str)->dict:
        ALGORITHM = "HS256"
        SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
        return jwt.decode(jwt=token,algorithms=ALGORITHM,key=SECRET_KEY)


if __name__ == '__main__':
    load_env()
    payload={
        "sub":str(uuid4()),
        "user_name":"winffee",
        "email":"xuchen.xia@outlook.com",
    }
    token = TokenUtil.create_access_token(payload)
    print(token)