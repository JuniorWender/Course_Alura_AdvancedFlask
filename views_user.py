from jogoteca import app
from flask import render_template, request, redirect, session, flash, url_for
from Users import Users
from helpers import UserForm
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    nextPage = request.args.get('next') # catch the value on quary string
    form = UserForm()
    return render_template('login.html', next=nextPage , title='Login', form=form)


@app.route('/logout')
def logout():
    session['logged_user'] = None # clear the session
    flash('No user logged!') # throw a message for user
    return redirect(url_for('index'))


@app.route('/auth', methods=['POST'])
def auth():
    form = UserForm(request.form) # catch the data of the form

    loginUser = Users.query.filter_by(nickname=form.username.data).first() # Verify if the user exists on db bring the nickname
    correctPassword = check_password_hash(loginUser.password, form.password.data) # Verify if the password is correct

    if loginUser and correctPassword: # if alredy exists verify the password 
        session['logged_user'] = loginUser.name # Save the user name on session
        flash(loginUser.name + ' Logged successfully!') # throw a message for user
        nextPage = request.form['next'] # catch the value on quary string for redirect to the page that the user was
        if nextPage == 'None':
            return redirect(url_for('index'))
        else:
            return redirect(nextPage)
    else:
        flash('Invalid user or password! Try again!') # throw a message for user
        return redirect(url_for('login'))