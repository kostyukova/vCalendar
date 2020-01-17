from swagger_server import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(255), index=True, unique=True)
    roles = db.Column(db.String(255))

    def __repr__(self):
        return 'User {}'.format(self.username)


class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)

    def __repr__(self):
        return 'Team {}'.format(self.name)


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


class Employee_total_days(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    total_days = db.Column(db.Integer)
    year = db.Column(db.Integer)

    def __repr__(self):
        return 'Employee {} has {} total days in {} year'\
            .format(self.employee_id, self.total_days, self.year)


class Employee_leave_days(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    leave_days = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def __repr__(self):
        return 'Employee {} leave days ({}, {})'\
            .format(self.employee_id, self.start_date, self.end_date)
