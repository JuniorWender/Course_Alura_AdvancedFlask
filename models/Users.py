from jogoteca import db

class Users(db.Model):
    nickname = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name