from flaskr.modules import authn
from .. import db
from flaskr.models import User

from flask import render_template, redirect, url_for, flash
from flask import session, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

@authn.route('/login', methods=['GET', 'POST'])
def login():
    """gets user credentials to login"""

    # If already logged in, send user to home page
    if 'user' in session:
        return redirect(url_for('views.home'))

    # if not logged in, login user
    else:
        if request.method == 'POST':

            email = request.form.get('email', '')
            password = request.form.get('password','')

            if password == '' and email == '':
                return render_template('login.html')

            else:
                # check if user exists
                user = User.query.filter_by(email=email).first()

                if user:

                    # if exist, check password
                    if check_password_hash(user.password, password):

                        # if right credentials, log in user
                        session['user'] = user.username
                        login_user(user, remember=True)
                        return redirect(url_for('views.home'))

                    # if wrong password, flash message
                    else:
                        flash('Incorrect password', category='error')
                        return render_template('login.html')

                # if email is not registered, flash message
                else:
                    flash('Email does not exist', category='error')
                    return render_template('login.html')

        else:
            return render_template('login.html')

@authn.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """get user new credentials to create an account"""

    # If already logged in, send user to home page
    if 'user' in session:
        return redirect(url_for('views.home'))

    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            fName = request.form.get('fName')
            lName = request.form.get('lName')
            username = request.form.get('username')

            """ check for already existing credentials in database """
            # check_email = db.session.query(User).filter_by(email=email).first()
            # check_username = db.session.query(User).filter_by(username=username).first()

            check_username = User.query.filter_by(username=username).first()
            check_email = User.query.filter_by(username=username).first()
            
            """ check alredy exising credentials and verify credential length"""
            if check_email:
                flash('This email is already registered with an account', category='error')
            
            elif check_username:
                flash('Username is already taken', category='error')

            elif len(username) < 3:
                flash('Invalid username! Use at least 3 characters.', category='error')

            elif len(password) < 3:
                flash('Password is to short', category='error')

            # if all good, create new user and add it to db
            else:
                new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'), first_name=fName, last_name=lName)
                db.session.add(new_user)
                db.session.commit()

                # login user
                login_user(new_user, remember=True)
                flash('Account created!')
                return redirect(url_for('authn.login'))

            return render_template('signUp.html')

        else:
            return render_template('signUp.html')

@authn.route('/logout')
@login_required
def logout():
    """ logout user """
    try:
        session.pop('user')
    except:
        print('user does not exits')

    if 'room' in session:
        session.pop('room')

    logout_user()
    return redirect(url_for('views.index'))