from swagger_server import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(255), index=True, unique=True)
    roles = db.Column(db.String(255))
    
    def __repr__(self):
        return 'User {}'.format(self.username)
