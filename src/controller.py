from dao import UserDAO , FriendDAO
from sqlalchemy.orm import Session
from models import User, Friend

class UserController:
    def __init__(self):
        pass

    @staticmethod
    def add_user(user:User) -> None:
        return UserDAO.add_user_to_database(user)
    
    @staticmethod
    def handle_login(email:str) -> None:
        return UserDAO.handle_login(email)
    
    @staticmethod
    def delete_user(id:int) ->None:
        return UserDAO.delete_user(id)
    
    @staticmethod
    def update_user(id:int,email:str,username:str) -> None:
        return UserDAO.update_user(id,email,username)
    

class FriendController:
    def __init__(self):
        pass


    @staticmethod
    def add_friend(friend:Friend) -> None:
        return FriendDAO.add_friend_todatabase(friend)
    
    @staticmethod 
    def remove_friend(id:int) -> None:
        return FriendDAO.remove_friend_fromdb(id)
    
    @staticmethod
    def update_friend(id:int,name:str, country:str, age:int , note:str) -> None:
        return FriendDAO.update_friend_fromdb(id,name,country,age,note)