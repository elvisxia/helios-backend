
from datetime import datetime

class UsersDAO:
    def __init__(self,postgresDB):
        self.postgresDB = postgresDB

    def get_user(self,user_name:str):
        cmd="select * from users where user_name = %s limit 1"
        res=self.postgresDB.fetch_one(sql=cmd,params=(user_name,))
        return res

    def insert_user(self,username:str,password_hash:str,full_name):
        cmd="insert into users(user_name,password_hash,full_name,create_time,last_login) values(%s,%s,%s,%s,%s)"
        res=self.postgresDB.execute(sql=cmd,params=(username,password_hash,full_name,str(datetime.now()),str(datetime.now())))
        return res

    def update_user(self,id:str,password_hash:str):
        cmd="update users set password_hash= %s where user_id = %s"
        res=self.postgresDB.execute(sql=cmd,params=(password_hash,id))
        return res

    def delete_user(self,id:str):
        cmd="delete from users where user_id = %s"
        return self.postgresDB.execute(sql=cmd,params=(id,))

if __name__=="__main__":
    from pwdlib import PasswordHash
    from utils.container import  container
    usersDAO=container.users_dao

    # 测试 insert_user
    hasher=PasswordHash.recommended()
    user_name="winffee"
    password="hudiai13"
    password_hashed=hasher.hash(password)
    print(password_hashed)
    full_name="Elvis Xia"
    #res=usersDAO.insert_user(user_name,password_hashed,full_name)
    #print(res)

    #测试get_user
    res=usersDAO.get_user(user_name)
    print("queried result:",res)
    queried_password=res['password_hash']
    res=hasher.verify(password,queried_password)
    print("verified result:",res)

    # 测试update_user





