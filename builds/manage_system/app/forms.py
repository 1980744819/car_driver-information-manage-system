from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators, IntegerField
from wtforms.validators import *
from app import app


class LoginForm(FlaskForm):
    user_id = StringField('user id', validators=[Required()])
    password = PasswordField('user password', validators=[Required(), Length(min=1, max=16)])
    remember_me = BooleanField('remember me', default=True)
    submit = SubmitField('Log In')


class SignInForm(FlaskForm):
    user_id = StringField('user id', validators=[Required(), Length(min=1, max=10)])
    name = StringField('user name', validators=[Required(), Length(min=4, max=32)])
    password = PasswordField('password', validators=[Required(), Length(min=1, max=16)])
    confirm_password = PasswordField('confirm password',
                                     validators=[Required(), Length(min=1, max=16), EqualTo('password', "not match")])
    submit = SubmitField('Sign In')


class DriverInfoUploadOrChangeForm(FlaskForm):
    driver_id = StringField('driver id', validators=[Required(), Length(min=1, max=10)])
    license_id = StringField('license id', validators=[Required(), Length(1, 20)])
    real_name = StringField('real name', validators=[Required(), Length(1, 32)])
    submit = SubmitField('Upload')


class AdminDriverInfoSearchOrDeleteForm(FlaskForm):
    driver_id = StringField('driver id', validators=[Required(), Length(min=1, max=10)])
    submit = SubmitField('Submit')


class CarInfoUploadOrChangeForm(FlaskForm):
    car_id = StringField('car id', validators=[Required(), Length(1, 32)])
    bought_time_year = StringField('the year bought', validators=[Required(), Length(4, 4)])
    bought_time_month = StringField('the month bought', validators=[Required(), Length(1, 2)])
    car_type = StringField('type of the car', validators=[Required(), Length(1, 32)])
    driver_id = StringField('driver id', validators=[])
    submit = SubmitField('Submit')


class CarInfoSearchOrDeleteForm(FlaskForm):
    car_id = StringField('car id', validators=[Required(), Length(1, 32)])
    submit = SubmitField('Submit')


class RepairRecordInfoUploadForm(FlaskForm):
    car_id = StringField('car id', validators=[Required(), Length(1, 32)])
    # record_id = IntegerField('repair record id', validators=[Required()])
    broken_time_year = StringField('the year broken', validators=[Required(), Length(4, 4)])
    broken_time_month = StringField('the month broken', validators=[Required(), Length(1, 2)])
    is_fixed = BooleanField('had it been fixed ?')
    fee = IntegerField('the money spent on this record', validators=[required()])
    submit = SubmitField('Submit')


class RepairRecordInfoChangeForm(FlaskForm):
    record_id = IntegerField('repair record id', validators=[Required()])
    car_id = StringField('car id', validators=[Required(), Length(1, 32)])
    broken_time_year = StringField('the year broken', validators=[Required(), Length(4, 4)])
    broken_time_month = StringField('the month broken', validators=[Required(), Length(1, 2)])
    is_fixed = BooleanField('had it been fixed ?')
    fee = IntegerField('the money spent on this record', validators=[required()])
    submit = SubmitField('Submit')


class RepairRecordInfoSearchOrDeleteForm(FlaskForm):
    id = IntegerField('the repair record id you want to delete', validators=[Required()])
    submit = SubmitField('Submit')


class InviteOrDeleteAdminForm(FlaskForm):
    id = StringField('admin id', validators=[Required(), Length(1, 10)])
    submit = SubmitField('Submit')


class DeleteUserForm(FlaskForm):
    id = StringField('user id', validators=[Required(), Length(1, 10)])
    submit = SubmitField('Submit')


class ChangeUserPasswordForm(FlaskForm):
    id = StringField('user id', validators=[Required(), Length(1, 10)])
    password = StringField('password', validators=[Required(), Length(1, 32)])
    submit = SubmitField('Submit')


class UserUploadDriverInfoForm(FlaskForm):
    driver_id = StringField('driver id', validators=[Required(), Length(min=1, max=10)])
    license_id = StringField('license id', validators=[Required(), Length(1, 20)])
    real_name = StringField('real name', validators=[Required(), Length(1, 32)])
    submit = SubmitField('Upload')


class NormalChangePassword(FlaskForm):
    id = StringField('user id', validators=[Required(), Length(1, 10)])
    old_password = StringField('old password', validators=[Required(), Length(1, 32)])
    new_password = StringField('new password', validators=[Required(), Length(1, 32)])
    confirm_password = PasswordField('confirm password',
                                     validators=[Required(), Length(min=1, max=16),
                                                 EqualTo('new_password', "not match")])
    submit = SubmitField('Submit')
