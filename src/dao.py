from models import User , Friend
from base import db
from flask import jsonify


class UserDAO:
    def __init__(self):
        pass

    @staticmethod
    def add_user_to_database(user:User) -> dict:
        existing_email = db.session.query(User).filter_by(
            email = user.email
        ).first()

        existing_username = db.session.query(User).filter_by(
            username = user.username
        ).first()

        
        if existing_email: 
            return jsonify({'status':'error','message':'Email already in use'})
        
        if existing_username:
            return jsonify({'status':'error','message':'Username already in use'})
        
        try:
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

            return jsonify({'status':'success'})
        
        except Exception as e:
            print('Error',e)
            return jsonify({'status':'error','message':'There was an issue while creating your account'})
    
    
    @staticmethod
    def delete_user(id:int) -> dict:
        existing_user = User.query.get_or_404(id)
        
        if not existing_user:
            return jsonify({'status':'error','message':'User does not exists'})
        
        try:
            db.session.delete(existing_user)
            db.session.commit()
            return jsonify({
                'status':'success'
            })
    
        except Exception as e:
            print('Error:',e)
            return jsonify({'status':'error','message':'There was an issue'})
        
    @staticmethod
    def update_user(id:int , email:str , username:str) -> dict:
        
        current_user = User.query.get_or_404(id)
        
        if not current_user:
            return jsonify({'status':'error','message':'User doesnt exists'})
        
        try:
            if email:
                current_user.email = email
            if username:
                current_user.username = username

            db.session.commit()
            return jsonify({
                'status':'success'
            })
        
        except Exception as e:
            print('Error',e)
            return jsonify({
                'status':'error',
                'message':'There was an issue updating your user'
            })


class FriendDAO:
    def __init__(self):
        pass

    
    @staticmethod
    def add_friend_todatabase(friend:Friend ) -> dict:
        try:
            db.session.add(friend)
            db.session.commit()
            db.session.refresh(friend)

            return jsonify({
                'status':'success',
                'friend':{
                    'id':friend.id,
                    'name':friend.name,
                    'country':friend.country,
                    'age':friend.age,
                    'note':friend.note
                }
            })
        
        except Exception as e:
            print('Error',e)
            return jsonify({
                'status':'error',
                'message':'There was an issue while adding your friend'
            })
        
    @staticmethod
    def remove_friend_fromdb(id:int) -> dict:
        current_friend = Friend.query.get_or_404(id)

        if not current_friend:
            return jsonify({'status':'success','message':'Friend does not exists'})
        
        try:
            db.session.delete(current_friend)
            db.session.commit()
            return jsonify({'status':'success'})
        
        except Exception as e:
            print('Error',e)
            return jsonify({'status':'error','message':'There was an issue deleting your friend'})
        
    @staticmethod
    def update_friend_fromdb(id:int,name:str,country:str,age:int,note:str) -> dict:
        current_friend = Friend.query.get_or_404(id)

        if not current_friend:
            return jsonify({'status':'error','message':'Friend doesnt exists'})
        
        try:
            if name:
                current_friend.name = name
            if country:
                current_friend.country = country
            if age :
                current_friend.age = age
            if note:
                current_friend.note = note
            
            db.session.commit()
            
            return jsonify({'status','success'})
        
        except Exception as e:
            print('Error',e)
            return jsonify({'status':'error','message':'There was an issue while updating your friend'})