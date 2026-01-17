from flask import Flask, request , url_for , redirect , render_template , jsonify , session
from werkzeug.security import generate_password_hash , check_password_hash
from models import User, Friend
from controller import FriendController , UserController
from base import db
import os
from functools import wraps
from dotenv import load_dotenv
import pymysql
from controller import UserController , FriendController

load_dotenv() # LOADING ENVIROMENT VARIABLES 

secret_key = os.getenv('secret_key')
database = os.getenv('database')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = secret_key
db.init_app(app=app) # INITIALIZING APPLICATION RIGHT HERE 

# ------- SOME HELPER METHODS RIGHT HERE --------- #

def get_frontend_form():
    data = request.form.to_dict()
    return data

def login_required(view):
    @wraps(view)

    def wrapped_view(*args,**kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return view(*args,**kwargs)
    return wrapped_view

# ------- Now Adjusting routes right here -------- # 

@app.route('/signup', methods = ['GET','POST'])
def signUp():
    
    if request.method == 'POST':
        
        data = get_frontend_form()
        new_user = User(
            email = data.get('email'),
            username = data.get('username'),
            password_hash= generate_password_hash(data.get('password'))
        )

        return UserController.add_user(new_user)
    return render_template('signup.html')


@app.route('/', methods = ['GET','POST'])
def login():

    if request.method == 'POST':

        data = get_frontend_form()
        
        existing_user = User.query.filter_by(
            email = data.get('email')
        ).first()

        
        if existing_user and check_password_hash(existing_user.password_hash , data.get('password')):
            try:
                session['user_id'] = existing_user.id
                return jsonify({'status':'success'})
            except Exception as e :
                print('Error:',e)
                return jsonify({
                'status':'error',
                'message':'There was an issue on your login'
                })
    return render_template('index.html')

@app.route('/logout')
@login_required
def account_logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/main')
@login_required
def mainPage():
    username = User.query.get(session['user_id']).username
    return render_template('main.html' , username = username)


@app.route('/api/friends')
@login_required
def api_friends_list():
    current_user_id = session['user_id']

    user_friends = Friend.query.filter_by(user_id=current_user_id).all()

    friends_data = [
        {
            'id': friend.id,
            'name': friend.name,
            'country': friend.country,
            'age': friend.age,
            'note': friend.note
        }
        for friend in user_friends
    ]

    return jsonify({
        'status': 'success',
        'friends': friends_data
    })


# --------- FRIENDS ROUTES ----------- # 

@app.route('/addFriend', methods = ['POST'])
@login_required
def add_friend_to_list():
    
        data = get_frontend_form()
        # GATHERING FRONTEND INFORMATION 

        name = data.get('name')
        country = data.get('country')
        age = data.get('age')
        note = data.get('note')

        new_friend = Friend(
            name = name,
            country = country,
            age = age ,
            note = note,
            user_id = session['user_id']
        )
        return FriendController.add_friend(new_friend)

@app.route('/update/friend/<int:id>' , methods = ['POST'])
@login_required
def update_friend_from_list(id:int):
    # GETTING USER PBY ID TO UPDATE HIM THEN
    existing_friend = Friend.query.get_or_404(id)
    
    if existing_friend.user_id != session['user_id']:
        return jsonify({'status':'error','message':'Unauthorized!'})
    
    # Gathering the atributes from the update formulary 
    data = get_frontend_form()
    name = data.get('name')
    country = data.get('country')
    age = data.get('age')
    note = data.get('note')

    return FriendController.update_friend(id,name,country,age,note,db)

@app.route('/delete/friend/<int:id>' , methods = ['POST'])
@login_required
def delete_friend_from_list(id:int):

    existing_friend = Friend.query.get_or_404(id)

    if existing_friend.user_id != session['user_id']:
        return jsonify({
            'status':'error',
            'message':'Unauthorized!'
        })
    
    return FriendController.remove_friend(id)


# ------------- USER ROUTES ------------- # 

@app.route('/profile' , methods = ['GET'])
@login_required
def profile_page():
    user = User.query.get(session['user_id'])
    return render_template('profile.html' , user = user)

@app.route('/update/user/<int:id>', methods = ['POST'])
@login_required
def update_account(id:int):
    data = get_frontend_form()
    return UserController.update_user(id,data.get('email'),data.get('username'))

@app.route('/delete/user/<int:id>' , methods = ['POST'])
@login_required
def delete_user_account(id:int):
    return UserController.delete_user(id)

        
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # CREATING ALL THE TABLES IN THE SCHEMA AFTER THE APPLICATION IS STARTED
    app.run(debug=True)
