from flaskr.modules import views
from flask import render_template, url_for, redirect
from flask import session, request
from flask_login import login_required, current_user
import random

@views.route('/')
def index():
    """page where the user will select to login or sign up"""
    return render_template('index.html')

@views.route('/home')
@login_required
def home():
    """ verify user is logged in"""
    if 'user' not in session:
        return redirect(url_for('authn.login'))

    return render_template('home.html', user=session['user'])

@views.route('/generate-key')
@login_required
def generate_key():

    """ verify user is logged in"""
    if 'user' not in session:
        return redirect(url_for('authn.login'))

    """Generate 2 random number between 100 - 1000. Put them together
    to create a random key shown in the frontend."""
    # generate a random key
    key1:int = random.randint(100,1000)
    key2:int = random.randint(100,1000)
    key:str = str(key1) + ' - ' + str(key2)

    # render template with key
    return render_template("generate_key.html", key=key)

@views.route('/join-room', methods=['GET', 'POST'])
@login_required
def join_room():

    """ verify user is logged in"""
    if 'user' not in session:
        return redirect(url_for('authn.login'))

    """ get username and room key. Then, save them in a session """
    if request.method == 'POST':
        "save room in session to connect client to room"
        session['room'] = request.form.get('roomKey', '')
        print(f"\nCredentials: {session['user']}, {session['room']}\n")
        
        return redirect(url_for('views.chat'))

    else:
        return render_template('join_room.html')

@views.route('/chat')
@login_required
def chat():

    """ verify user is logged in"""
    if 'user' not in session:
        return redirect(url_for('authn.login'))
    
    # verify user entered a room
    elif 'room' not in session:
        return redirect(url_for('views.join_room'))

    else:
        """verify username and room. If they aren't valid, redirect user 
        to join_room to enter credentials again. Else, send user to chat room"""
        # verify credentials
        name = session['user']
        room = session['room']

        if len(name) < 3 or len(room) != 9:
            return redirect(url_for('views.join_room'))
        
        # enter chat room
        else:
            return render_template('chat_room.html', name=name, room=room)