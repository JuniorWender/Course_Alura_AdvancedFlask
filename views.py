from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
import time

from jogoteca import app, db

from Games import Games
from Users import Users
from helpers import recovery_Image, deleta_arquivo, GameForm

# ------------------------------------------------- Pages Routes ----------------------------------------------------------------

@app.route('/')
def index():
    list = Games.query.order_by(Games.id) # select * from games
    return render_template('gameTable.html', title='Games', games=list)

@app.route('/new')
def new():
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('login', next=url_for('new'))) # quary string
    form = GameForm()
    return render_template('create.html', title='create A New Game', form=form)

@app.route('/edit/<int:id>')
def edit(id):
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('login', next=url_for('edit'))) # quary string
    editGame = Games.query.filter_by(id=id).first()

    form = GameForm() # create a form object
    form.name.data = editGame.name # set the data of the form
    form.category.data = editGame.category # set the data of the form
    form.plataform.data = editGame.plataform # set the data of the form

    editGame.img = recovery_Image(editGame.id) # call the function to recovery the game image

    return render_template('edit.html', title='Edit {} '.format(editGame.name), id=id, gameCover=editGame.img, form=form )

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
    form = GameForm(request.form) # catch the data of the form

    if not form.validate_on_submit(): # verify if the form is valid
        return redirect(url_for('new'))
    
    name = form.name.data
    category = form.category.data
    plataform = form.plataform.data
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
    timestamp = time.time() # catch the timestamp for rename the image

    file.save(f'{upload_path}/gameCover_{newGame.id}-{timestamp}.jpg') # save the image on folder img with the id of the game

    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    form = GameForm(request.form) # catch the data of the form

    if form.validate_on_submit(): # verify if the form is valid
        databaseGame = Games.query.filter_by(id=request.form['id']).first()
        databaseGame.name = form.name.data
        databaseGame.category = form.category.data
        databaseGame.plataform = form.plataform.data

        db.session.add(databaseGame)
        db.session.commit()

        file = request.files['imgFile'] # catch the image file

        upload_path = app.config['UPLOAD_PATH'] # catch the path of the folder img
        timestamp = time.time() # catch the timestamp for rename the image
        deleta_arquivo(databaseGame.id)

        file.save(f'{upload_path}/gameCover_{databaseGame.id}-{timestamp}.jpg') # save the image on folder img with the id of the game

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
