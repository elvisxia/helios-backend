
class UserDAO:
    def __init__(self,postgresDB):
        self.postgresDB = postgresDB

    def get_user(self,username:str,password_hash:str):
        cmd="select top 1 from user where username = %s and password_hash = %s"
        self.postgresDB.cursor().execute(cmd,(username,password_hash))