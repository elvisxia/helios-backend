from utils.hash_util import HashUtil
from utils.token_util import TokenUtil
from datetime import datetime, timedelta


class UserService:
    def __init__(self,userDAO):
        self.userDAO=userDAO

    def login_user(self,user_name:str,password:str):
        res={
            'user':None,
            'login_success':False,
            'token':None,
        }
        user=self.userDAO.get_user(user_name=user_name)
        if user is None:
            return res
        # verify password hash
        login_success=HashUtil.verify_password(password=password,hashed_password=user['password_hash'])
        if login_success:
            del user['password_hash']
            res['user']=user
            res['login_success']=True
            user['exp']=datetime.now()+timedelta(hours=24)
            token=TokenUtil.create_access_token(payload=user)
            res['token']=token
        return res





if __name__=="__main__":
    from utils.container import container
    user_service=container.user_service
    res=user_service.login_user(user_name='winffee',password='hudiai13')
    print(res)