from flask import Flask, render_template, flash, url_for, redirect, session
from datetime import datetime
from .forms import *
from .models import *
from app import app, db
from . import main
from flask_login import login_user, login_required, logout_user, current_user


def flash_success(message):
    return flash(message, 'success')


def flash_warning(me):
    return flash(me, 'warning')


def db_upload(form_data, query_result):
    if query_result is None:
        db.session.add(form_data)
        db.session.commit()
        flash_success('success')
    else:
        flash_warning('record do exit! maybe you want to change or search')


def db_change(form_data, query_result):
    if query_result is None:
        flash_warning('record do not exit! maybe you wan to upload')
    else:
        query_result = form_data
        db.session.add(query_result)
        db.session.commit()
        flash_success('success!')


def user_is_exit(user_id):
    query_result = User.query.filter_by(user_id=user_id).first()
    if query_result is None:
        return False
    else:
        return True


def admin_is_exit(user_id):
    query_result = Admin.query.filter_by(admin_id=user_id).first()
    if query_result is None:
        return False
    return True


def admin_delete(user_id):
    query_result = Admin.query.filter_by(admin_id=user_id).first()
    if query_result is None:
        flash_warning('admin do not exit')
    else:
        db.session.delete(query_result)
        db.session.commit()
        flash_success('success')


def car_is_exit(car_id):
    query_result = CarInfo.query.filter_by(car_id=car_id).first()
    if query_result is None:
        return False
    else:
        return True


# def user_join(form_data):
#     new_user = User(user_id=form_data.user_id, nick_name=form_data.name, password=form_data.password)
#     db.session.add(new_user)
#     db.session.commit()
#     flash_success('success')


def user_delete(user_id):
    query_result = User.query.filter_by(user_id=user_id).first()
    if query_result is None:
        flash_warning('user had already deleted!')
    else:
        db.session.delete(query_result)
        db.session.commit()
        flash_success('success')


def delete_info(query_result, ms):
    if query_result is None:
        flash_warning(ms + ' information does not exit')
    else:
        db.session.delete(query_result)
        db.session.commit()
        flash_success('success')


def search_info(query_result, ms):
    if query_result is None:
        flash_warning(ms + ' information does not exit')
    else:
        print("111111")
        return redirect(url_for('.search_result', query_result=query_result))


@app.route('/admin/search_result', methods=['GET', 'POST'])
def search_result(query_result):
    print("22222222")
    return render_template('search_result.html', query_result=query_result)


@app.route('/')
def home():
    # logout_user()
    return render_template("home.html", current_time=datetime.utcnow())


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You Have Been Logged Out')
    return redirect(url_for('home'))


@app.route('/<username>')
@login_required
def normal_user(username):
    form = UserUploadDriverInfoForm()
    if form.validate_on_submit():
        if current_user.user_id == form.driver_id.data:
            query_result = User.query.filter_by(driver_id=form.driver_id.data).first()
            query_result.license_id = form.license_id.data
            query_result.real_name = form.real_name.data
            db.session.add(query_result)
            db.session.commit()
            flash_success('success')
        else:
            flash_warning('user id is not correct')

    driver_query = DriverInfo.query.filter_by(driver_id=current_user.user_id).first()
    car_query_results = CarInfo.query.filter_by(driver_id=current_user.user_id).all()
    if driver_query is None:
        license_id = None
        real_name = None
    else:
        license_id = driver_query.license_id
        real_name = driver_query.real_name
    user_id = current_user.user_id
    nick_name = current_user.nick_name
    password = current_user.password
    cars = len(car_query_results)
    dic = {
        "用户编号": user_id,
        "昵称": nick_name,
        "密码": password,
        "驾照编号": license_id,
        "姓名": real_name,
        "驾驶车辆数": cars
    }
    return render_template('normal_user.html', form=form, query_result=dic, current_time=datetime.utcnow())


@app.route('/<username>/change_password')
def normal_change_password(username):
    form = NormalChangePassword()
    return render_template('normal_change_password.html', form=form, current_time=datetime.utcnow())


@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data, password=form.password.data).first()
        # print(user.id, user.user_id, user.nick_name, user.password)
        if user is not None:
            print("found")
            login_user(user, form.remember_me.data)
            admin_user = Admin.query.filter_by(admin_id=form.user_id.data).first()
            if admin_user is None:
                print("normal user")
                return redirect(url_for('normal_user', _external=True, username=current_user.nick_name))
            else:
                print("Admin")
                # print(current_user.user_id)
                return redirect(url_for('.admin'))
        flash('Invalid username or password', 'warning')
        form.user_id.data = ''
        form.password.data = ''
        return redirect(url_for('.login'))
    return render_template('login.html', form=form, user_id=session.get('user_id'), password=session.get('password'),
                           current_time=datetime.utcnow())


@app.route('/admin')
@login_required
def admin():
    # print(current_user.id)
    return render_template('admin.html', current_time=datetime.utcnow())


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data)
        print(user)
        if user is None:
            flash('This ID has been registered!', 'warning')
            return redirect(url_for('.signin'))
        else:
            info = User(user_id=form.user_id.data, nick_name=form.name.data, password=form.password.data)
            db.session.add(info)
            db.session.commit()
            form.name.data = ''
            form.password.data = ''
            return redirect(url_for('.login'))
    return render_template('signin.html', form=form, name=session.get('name'), current_time=datetime.utcnow())


@app.route('/<username>/driver_info_upload', methods=['GET', 'POST'])
def driver_info_upload(username):
    form = DriverInfoUploadOrChangeForm()
    if form.validate_on_submit():
        driver_info_data = DriverInfo(driver_id=form.driver_id.data, license_id=form.license_id.data,
                                      real_name=form.real_name.data)

        user_query_result = User.query.filter_by(user_id=driver_info_data.driver_id).first()
        print(type(user_query_result))
        print(user_query_result)
        if user_query_result is not None:

            driver_info_query_result = DriverInfo.query.filter_by(driver_id=driver_info_data.driver_id).first()
            if driver_info_query_result is None:
                db.session.add(driver_info_data)
                db.session.commit()
                print("Yes")
                flash("Success", 'success')
            else:
                print("No")
                flash("Driver information already exit!", 'warning')
        else:
            print("driver id do not exit")
            flash("driver id do not exit", 'warning')
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/<username>/driver_info_change', methods=['GET', 'POST'])
def driver_info_change(username):
    form = DriverInfoUploadOrChangeForm()
    if form.validate_on_submit():
        driver_info_data = DriverInfo(driver_id=form.driver_id.data, license_id=form.license_id.data,
                                      real_name=form.real_name.data)
        user_query_result = User.query.filter_by(user_id=driver_info_data.driver_id).first()
        if user_query_result is not None:
            driver_info_query_result = DriverInfo.query.filter_by(driver_id=driver_info_data.driver_id).first()
            if driver_info_query_result is None:
                flash('driver information do not exit, you should try to upload', 'warning')
            else:
                driver_info_query_result.license_id = driver_info_data.license_id
                driver_info_query_result.real_name = driver_info_data.real_name
                db.session.add(driver_info_query_result)
                db.session.commit()
                flash('success', 'success')
        else:
            flash('user do not exit')
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/driver_info_search', methods=['GET', 'POST'])
def admin_driver_info_search():
    form = AdminDriverInfoSearchOrDeleteForm()
    if form.validate_on_submit():
        if user_is_exit(form.driver_id.data):
            query_result = DriverInfo.query.filter_by(driver_id=form.driver_id.data).first()
            # search_info(query_result, 'driver')
            if query_result is None:
                flash_warning('driver information do not exit')
            else:
                print(query_result.__dict__)
                result = {"姓名": query_result.real_name,
                          "用户 ID": query_result.driver_id,
                          "驾照 ID": query_result.license_id,
                          }
                return render_template('search_result.html', query_result=result, current_time=datetime.utcnow())
        else:
            flash_warning('user do not exit!')
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/driver_info_delete', methods=['GET', 'POST'])
def admin_driver_info_delete():
    form = AdminDriverInfoSearchOrDeleteForm()
    if form.validate_on_submit():
        if user_is_exit(form.driver_id.data):
            query_result = DriverInfo.query.filter_by(driver_id=form.driver_id.data).first()
            delete_info(query_result, 'driver')
        else:
            flash_warning('user do not exit!')
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/car_info_upload', methods=['GET', 'POST'])
def admin_car_info_upload():
    form = CarInfoUploadOrChangeForm()
    if form.validate_on_submit():
        form_data = CarInfo(car_id=form.car_id.data,
                            bought_time=form.bought_time_year.data + "/" + form.bought_time_month.data,
                            car_type=form.car_type.data, driver_id=form.driver_id.data)
        if form_data.driver_id == "":
            form_data.driver_id = '2015014325'
        query_result = CarInfo.query.filter_by(car_id=form_data.car_id).first()
        if user_is_exit(form_data.driver_id):
            db_upload(form_data, query_result)
        else:
            flash_warning("driver id do not exit")
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/car_info_change', methods=['GET', 'POST'])
def admin_car_info_change():
    form = CarInfoUploadOrChangeForm()
    if form.validate_on_submit():
        form_data = CarInfo(car_id=form.car_id.data,
                            bought_time=form.bought_time_year.data + '/' + form.bought_time_month.data,
                            car_type=form.car_type.data, driver_id=form.driver_id.data)
        if form_data.driver_id == "":
            form_data.driver_id = '2015014325'
        print("11111111111111111111111111111111")
        print(form_data.driver_id, "1111111")
        print("1111111111111111111")
        if user_is_exit(form_data.driver_id):
            query_result = CarInfo.query.filter_by(car_id=form_data.car_id).first()
            if query_result is None:
                flash_warning('record do not exit! maybe you wan to upload')
            else:
                query_result.bought_time = form_data.bought_time
                query_result.car_type = form_data.car_type
                query_result.driver_id = form_data.driver_id
                # query_result = form_data
                db.session.add(query_result)
                db.session.commit()
                flash_success('success!')
                # db_change(form_data, query_result)
        else:
            flash_warning("driver id do not exit")
            # db_change(form_data, query_result)

    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/car_info_search', methods=['GET', 'POST'])
def admin_car_info_search():
    form = CarInfoSearchOrDeleteForm()
    if form.validate_on_submit():
        query_result = CarInfo.query.filter_by(car_id=form.car_id.data).first()
        if query_result is not None:
            result = {
                "车辆编号": query_result.car_id,
                "购买时间": query_result.bought_time,
                "车辆型号": query_result.car_type,
                "驾驶人ID": query_result.driver_id
            }
            return render_template('search_result.html', query_result=result, current_time=datetime.utcnow())
        else:
            flash_warning('car do not exit!')
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/car_info_delete', methods=['GET', 'POST'])
def admin_car_info_delete():
    form = CarInfoSearchOrDeleteForm()
    if form.validate_on_submit():
        query_result = CarInfo.query.filter_by(car_id=form.car_id.data).first()
        delete_info(query_result, 'car')
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/repair_record_info_upload', methods=['GET', 'POST'])
def repair_record_info_upload():
    form = RepairRecordInfoUploadForm()
    if form.validate_on_submit():

        form_data = RepairRecord(car_id=form.car_id.data,
                                 broken_time=form.broken_time_year.data + '/' + form.broken_time_month.data,
                                 is_fixed=form.is_fixed.data, fee=form.fee.data)
        if car_is_exit(form_data.car_id):
            # query_result = RepairRecord.query.filter_by(record_id=form_data.record_id).first()
            # db_upload(form_data, query_result)
            db.session.add(form_data)
            db.session.commit()
            extra_message = "record id: " + str(form_data.id)
            flash('success ', 'success')
            return render_template('operations.html', form=form, extra_message=extra_message,
                                   current_time=datetime.utcnow())
        else:
            flash_warning('car do not exit!')
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/repair_record_info_change', methods=['GET', 'POST'])
def repair_record_info_change():
    form = RepairRecordInfoChangeForm()
    if form.validate_on_submit():
        form_data = RepairRecord(car_id=form.car_id.data,
                                 broken_time=form.broken_time_year.data + '/' + form.broken_time_month.data,
                                 is_fixed=form.is_fixed.data, fee=form.fee.data)
        form_data.id = form.record_id.data
        if car_is_exit(form_data.car_id):
            query_result = RepairRecord.query.filter_by(id=form_data.id).first()
            if query_result is not None:
                query_result.car_id = form_data.car_id
                query_result.broken_time = form_data.broken_time
                query_result.is_fixed = form_data.is_fixed
                query_result.fee = form_data.fee
                db.session.add(query_result)
                db.session.commit()
                flash_success('sucess')
            else:
                flash_warning('record id do not exit')
        else:
            flash_warning('car do not exit')
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/repair_record_info_search', methods=['GET', 'POST'])
def repair_record_info_search():
    form = RepairRecordInfoSearchOrDeleteForm()
    if form.validate_on_submit():
        query_result = RepairRecord.query.filter_by(id=form.id.data).first()
        if query_result is not None:
            if query_result.is_fixed:
                is_fix = '是'
            else:
                is_fix = '否'
            result = {
                "维修编号": query_result.id,
                "车辆编号": query_result.car_id,
                "损坏时间": query_result.broken_time,
                "是否修好": is_fix,
                "修理花费": query_result.fee
            }
            return render_template('search_result.html', query_result=result, current_time=datetime.utcnow())
        else:
            flash_warning('car do not exit!')

    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/repair_record_info_delete', methods=['GET', 'POST'])
def repair_record_info_delete():
    form = RepairRecordInfoSearchOrDeleteForm()
    if form.validate_on_submit():
        query_result = RepairRecord.query.filter_by(id=form.id).first()
        if query_result is None:
            flash_warning('record do not exit')
        else:
            delete_info(query_result, 'record')
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/invite_admin', methods=['GET', 'POST'])
def invite_admin():
    form = InviteOrDeleteAdminForm()
    if form.validate_on_submit():
        user_id = form.id.data
        if user_is_exit(user_id):
            if admin_is_exit(user_id):
                flash_warning('admin already exit!')
            else:
                admin_user = Admin(admin_id=user_id)
                db.session.add(admin_user)
                db.session.commit()
                flash_success('sucess')
        else:
            flash_warning('user id do not exit')
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/delete_admin', methods=['GET', 'POST'])
def delete_admin():
    form = InviteOrDeleteAdminForm()
    if form.validate_on_submit():
        user_id = form.id.data
        if user_is_exit(user_id):
            admin_delete(user_id)
        else:
            flash_warning('user id do not exit')
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/join_user', methods=['GET', 'POST'])
def join_user():
    form = SignInForm()
    if form.validate_on_submit():
        # user_id = form.user_id.data
        if user_is_exit(form.user_id.data):
            flash_warning('user already do exit!')
        else:
            form_data = User(user_id=form.user_id.data, nick_name=form.name.data, password=form.password.data)
            db.session.add(form_data)
            db.session.commit()
            flash_success('success!')
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/delete_user', methods=['GET', 'POST'])
def delete_user():
    form = DeleteUserForm()
    if form.validate_on_submit():
        user_delete(form.id.data)
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangeUserPasswordForm()
    if form.validate_on_submit():
        query_result = User.query.filter_by(user_id=form.id.data).first()
        if query_result is None:
            flash_warning("user do not exit!")
        else:
            query_result.password = form.password.data
            db.session.add(query_result)
            db.session.commit()
            flash_success('success')
    return render_template('operations.html', form=form, current_time=datetime.utcnow())


@app.route('/admin/menu', methods=['GET', 'POST'])
def admin_menu():
    return render_template("admin_menu.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", current_time=datetime.utcnow())
