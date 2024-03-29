import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app_name = app.config['APP_NAME']
login = LoginManager(app)
# login.login_view = 'login'

class MyAdminIndex(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def _handle_view(self, name, **kwargs):
        """
            This method will be executed before calling any view method.

            By default, it will check if the admin class is accessable
            and if it is NOT it will throw a 404.

            :param name:
                View function name
            :param kwargs:
                View function arguments
        """
        if not self.is_accessible():
            return redirect(url_for("login"))


from app import routes, models, errors
admin = Admin(app, name=f'{app_name} Admin Panel', index_view=MyAdminIndex())
admin.add_view(ModelView(models.Post, db.session))
admin.add_link(MenuLink(name='Sign Out', url='/logout'))
app.config['FLASK_ADMIN_SWATCH'] = 'cyborg'


# ERROR LOGGING TO EMAIL
# if not app.debug:
    # if app.config['MAIL_SERVER']:
        # auth = None
        # if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            # auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
       # secure = None
        # if app.config['MAIL_USE_TLS']:
            # secure = ()
        # mail_handler = SMTPHandler(
            # mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            # fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            # toaddrs=app.config['ADMINS'], subject='Musicblog Failure',
            # credentials=auth, secure=secure)
        # mail_handler.setLevel(logging.ERROR)
        # app.logger.addHandler(mail_handler)

# ERROR Logging to file
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/musicblog.log', maxBytes=10240,
                                    backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Musicblog startup')

