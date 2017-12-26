from flask import Flask, Blueprint
from flask_moment import Moment
# from flask.ext.bootstrap import Bootstrap
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

main = Blueprint('main', __name__)
app.register_blueprint(main)

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'login'
login_manager.init_app(app)


# def make_shell_context():
#     return dict(app=app, db=db)
#
#
# manager.add_command("shell", Shell(make_context=make_shell_context()))
manager.add_command('db', MigrateCommand)

from app import views, models
