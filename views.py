from flask import render_template, request, redirect, session, flash, url_for

from jogoteca import app, db

from models import Games
from models.Users import Users

# ------------------------------------------------- Pages Routes ----------------------------------------------------------------

@app.route('/')
def index():
    list = Games.query.order_by(Games.id) # select * from games
    return render_template('gameTable.html', title='Games', games=list)

@app.route('/new')
def new():
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('login', next=url_for('new'))) # quary string
    return render_template('register.html', title='Register A New Game')

@app.route('/login')
def login():
    nextPage = request.args.get('next') # catch the value on quary string
    return render_template('login.html', next=nextPage , title='Login')


# ------------------------------------------------- Methods Routes ----------------------------------------------------------------

@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    category = request.form['category']
    plataform = request.form['plataform']
    game = Games.query.filter_by(name=name).first() # verify if the game already exists

    if game:  # if exists, return to index
        flash('Game ' + name + ' already exists!')
        return redirect(url_for('index'))
    
    # else, create a new game

    newGame = Games(name=name, category=category, plataform=plataform) # create a object with data for persist on db
    db.session.add(newGame) # add data on db
    db.session.commit() # persist data on db
    return redirect(url_for('index'))


@app.route('/auth', methods=['POST'])
def auth():
    loginUser = Users.query.filter_by(nickname=request.form['user']).first() # Verify if the user exists on db bring the nickname
    if loginUser: # if alredy exists verify the password
        if request.form['password'] == loginUser.password: # if the password is correct, log the user
            session['logged_user'] = loginUser.name # Save the user name on session
            flash(loginUser.name + ' Logged successfully!') # throw a message for user
            nextPage = request.form['next'] # catch the value on quary string for redirect to the page that the user was
            return redirect(nextPage)
    else:
        flash('Invalid user or password! Try again!') # throw a message for user
        return redirect(url_for('login'))
    

@app.route('/logout')
def logout():
    session['logged_user'] = None # clear the session
    flash('No user logged!') # throw a message for user
    return redirect(url_for('index'))