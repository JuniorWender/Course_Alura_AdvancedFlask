from flask import Flask, render_template, request, redirect, session, flash, url_for

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'crypto'

app.config['SQLALCHEMY_DATABASE_URI'] = '{SGBD}://{user}:{password}@{server}/{database}'.format(
    SGBD='mysql+mysqlconnector',
    user='root',
    password='root',
    server='localhost',
    database='jogoteca'
)

db = SQLAlchemy(app)

class Games(db.Model):
    id = db.column(db.Integer, primary_key=True, autoincrement=True),
    name = db.column(db.String(50), nullable=False),
    category = db.column(db.String(40), nullable=False),
    plataform = db.column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
    
class Users(db.Model):
    nickname = db.column(db.String(10), primary_key=True),
    name = db.column(db.String(20), nullable=False),
    password = db.column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

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