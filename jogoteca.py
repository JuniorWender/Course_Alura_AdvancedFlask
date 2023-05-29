from flask import Flask, render_template, request, redirect, session, flash, url_for

class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console

game1 = Game('Tetris', 'Puzzle', 'Super Nintendo')
game2 = Game('Super Mario', 'Action', 'Super Nintendo')
game3 = Game('Mortal Kombat', 'Fight', 'PS2')
game4 = Game('Skyrim', 'RPG', 'PC')
list = [game1, game2, game3,game4]

class User:
    def __init__(self, name, nickname, password):
        self.name = name
        self.nickname = nickname
        self.password = password

user1 = User('admin', 'o Admin', 'admin')
user2 = User('user', 'usuario', 'user')
users = {user1.name: user1, user2.name: user2}


app = Flask(__name__)
app.secret_key = 'criptografia'

# ------------------------------------------------- Pages ----------------------------------------------------------------
@app.route('/')
def index():
    return render_template('gameTable.html', title='Games', games=list)

@app.route('/new')
def new():
    if 'logged_user' not in session or session['logged_user'] == None:
        return redirect(url_for('login', next=url_for('new'))) # quary string
    return render_template('register.html', title='Register A New Game')

@app.route('/login')
def login():
    nextPage = request.args.get('next') # Captura o valor do quary string
    return render_template('login.html', next=nextPage , title='Login')

# ------------------------------------------------- Methods ----------------------------------------------------------------
@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    category = request.form['category']
    plataform = request.form['plataform']
    game = Game(name, category, plataform)
    list.append(game)
    return redirect(url_for('index'))

@app.route('/auth', methods=['POST'])
def auth():
    if request.form['user'] in users:
        user = users[request.form['user']]
        if request.form['password'] == user.password:
            session['logged_user'] = user.name
            flash(user.name + ' Logged successfully!')
            nextPage = request.form['next']
            return redirect(nextPage)
    else:
        flash('Invalid user or password! Try again!')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['logged_user'] = None
    flash('No user logged!')
    return redirect(url_for('index'))

app.run(debug=True)