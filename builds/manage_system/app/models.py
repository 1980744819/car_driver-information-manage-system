from app import db
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'user_list'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(10), unique=True, nullable=False)
    nick_name = db.Column(db.Unicode(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)

    def __init__(self, user_id, nick_name, password):
        self.user_id = user_id
        self.nick_name = nick_name
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.nick_name

    def is_admin(self):
        query_result = Admin.query.filter_by(admin_id=self.user_id).first()
        if query_result is None:
            return False
        else:
            return True


class Admin(db.Model):
    __tablename__ = 'admin_list'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(10), db.ForeignKey('user_list.user_id'))

    def __init__(self, admin_id):
        self.admin_id = admin_id

    def __repr__(self):
        return '<Admin %r>' % self.id


class DriverInfo(db.Model):
    __tablename__ = 'driver_info_list'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.String(10), db.ForeignKey('user_list.user_id'))
    license_id = db.Column(db.String(20), unique=True)
    real_name = db.Column(db.Unicode(32))

    def __init__(self, driver_id, license_id, real_name):
        self.driver_id = driver_id
        self.license_id = license_id
        self.real_name = real_name

    def __repr__(self):
        return '<Driver %r>' % self.real_name


class CarInfo(db.Model):
    __tablename__ = 'car_info_list'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.String(32), unique=True)
    # used_time = db.Column(db.String(10))
    bought_time = db.Column(db.String(10))
    car_type = db.Column(db.String(32))
    driver_id = db.Column(db.String(10), db.ForeignKey('user_list.user_id'))

    def __init__(self, car_id, bought_time, car_type, driver_id):
        self.car_id = car_id
        self.bought_time = bought_time
        self.car_type = car_type
        self.driver_id = driver_id

    def __repr__(self):
        return '<Car %r>' % self.car_id


class RepairRecord(db.Model):
    __tanblename__ = 'repair_record_list'
    id = db.Column(db.Integer, primary_key=True)
    # record_id = db.Column(db.Integer)
    car_id = db.Column(db.String(32), db.ForeignKey('car_info_list.car_id'))
    broken_time = db.Column(db.String(10))
    is_fixed = db.Column(db.Boolean)
    fee = db.Column(db.Integer)

    def __init__(self, car_id, broken_time, is_fixed, fee):
        # self.record_id = record_id
        self.car_id = car_id
        self.broken_time = broken_time
        self.is_fixed = is_fixed
        self.fee = fee

    def __repr__(self):
        return '<repair_record %r>' % self.car_id
