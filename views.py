from flask import render_template, request, redirect, session, flash, url_for, send_from_directory

from jogoteca import app, db

from Games import Games
from Users import Users
from helpers import recovery_Image

# ------------------------------------------------- Pages Routes ----------------------------------------------------------------

@app.route('/')
def index():
    list = Games.query.order_by(Games.id) # select * from games
    return render_template('gameTable.html', title='Games', games=list)

@app.route('/new')
def new():
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('login', next=url_for('new'))) # quary string
    return render_template('create.html', title='create A New Game')

@app.route('/edit/<int:id>')
def edit(id):
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('login', next=url_for('edit'))) # quary string
    editGame = Games.query.filter_by(id=id).first()
    editGame.img = recovery_Image(editGame.id) # call the function to recovery the game image

    return render_template('edit.html', title='Edit {} '.format(editGame.name), editGame=editGame, gameCover=editGame.img )

@app.route('/delete/<int:id>')
def delete(id):
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('login')) 
    Games.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Game deleted successfully!')
    return redirect(url_for('index'))

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

    file = request.files['imgFile'] # catch the image file

    upload_path = app.config['UPLOAD_PATH'] # catch the path of the folder img

    file.save(f'{upload_path}/gameCover_{newGame.id}.jpg') # save the image on folder img with the id of the game

    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    databaseGame = Games.query.filter_by(id=request.form['id']).first()
    databaseGame.name = request.form['name']
    databaseGame.category = request.form['category']
    databaseGame.plataform = request.form['plataform']

    db.session.add(databaseGame)
    db.session.commit()

    file = request.files['imgFile'] # catch the image file

    upload_path = app.config['UPLOAD_PATH'] # catch the path of the folder img

    file.save(f'{upload_path}/gameCover_{databaseGame.id}.jpg') # save the image on folder img with the id of the game

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

@app.route('/upload/<game_Cover>')
def image(game_Cover):
    return send_from_directory('upload', game_Cover) # return the image for the page
