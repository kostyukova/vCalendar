from swagger_server import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(255), index=True, unique=True)
    roles = db.Column(db.String(255))

    def __repr__(self):
        return 'User {}'.format(self.username)


class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), index=True)
    position = db.Column(db.String(20))
    specialization = db.Column(db.String(20))
    team_id = db.Column(db.Integer, index=True, unique=True)
    expert = db.Column(db.Boolean)
    email = db.Column(db.String(255), index=True, unique=True)

    def __repr__(self):
        return 'Employee {}'.format(self.full_name)
