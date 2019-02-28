from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_migrate import Migrate
from flask_mail import Mail
from flask_uploads import IMAGES, UploadSet
# from solarvibes.admin.views import admin


photos =  UploadSet('photos', IMAGES)               # Flask-Uploads
db = SQLAlchemy()                                # create database connection object
migrate = Migrate()                          # creates a migration object for the application db migrations]\
mail = Mail()
security = Security()


def create_app():
    # general imports
    #############################
    from flask import Flask
    from flask_security import SQLAlchemyUserDatastore
    from solarvibes.forms import RegisterFormExt
    from flask_uploads import configure_uploads
    from solarvibes.config import Config

    # models import
    #############################
    from solarvibes.models import roles_users, Role, User
    from solarvibes.models import Farm, Field, DailyFieldInput, Crop
    from solarvibes.models import Agrimodule, Agrisensor, Measurement, Agripump, Pump
    from solarvibes.site.models import NewsletterTable, AgrimoduleFBTable, PlatformFBTable, WorkWithUsTable, ContactUsTable

    # App initilization and configuration
    #####################################
    application = Flask(__name__)                               # creates the flask application
    application.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'       # Flask-Uploads
    application.config.from_object(Config)                   # imports application configuration from config.py

    # init external packages
    #####################################
    configure_uploads(application, photos)
    db.init_app(application)
    migrate.init_app(application, db)
    mail.init_app(application)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(application, user_datastore, register_form=RegisterFormExt, confirm_register_form=RegisterFormExt)
    # admin.init_app(application)

    # blueprint imports
    #############################
    from solarvibes.boot.views import boot
    from solarvibes.app.views import app
    from solarvibes.site.views import site
    from solarvibes.users.views import users
    from solarvibes.welcome.views import welcome
    from solarvibes.main.views import main
    from solarvibes.settings.views import settings
    from solarvibes.farm_settings.views import farm_settings
    from solarvibes.agrimodule_settings.views import agrimodule_settings
    from solarvibes.pump_settings.views import pump_settings
    from solarvibes.agrimodule.views import agrimodule_bp
    from solarvibes.agripump.views import agripump_bp
    from solarvibes.crop_status.views import crop_status
    from solarvibes.login_check.views import login_check
    # from solarvibes.admin.views import admin_bp
    from solarvibes.agrimodule_api.views_new import agrimodule_api
    from solarvibes.crop_planning.views import crop_planning_bp

    # blueprint registration
    #############################
    application.register_blueprint(boot, url_prefix='/')
    application.register_blueprint(app, url_prefix='/app')
    application.register_blueprint(site, url_prefix='/site')
    application.register_blueprint(users, url_prefix='/users')
    application.register_blueprint(welcome, url_prefix='/welcome')
    application.register_blueprint(main, url_prefix='/main')
    application.register_blueprint(settings, url_prefix='/settings')
    application.register_blueprint(farm_settings, url_prefix='/farm-settings')
    application.register_blueprint(agrimodule_settings, url_prefix='/agrimodule-settings')
    application.register_blueprint(pump_settings, url_prefix='/pump-settings')
    application.register_blueprint(agrimodule_bp, url_prefix='/agrimodule')
    application.register_blueprint(agripump_bp, url_prefix='/agripump')
    application.register_blueprint(crop_status, url_prefix='/crop-status')
    application.register_blueprint(login_check, url_prefix='/login-check')
    # application.register_blueprint(admin_bp, url_prefix='/admin')
    application.register_blueprint(agrimodule_api, url_prefix='/agrimodule_api')
    application.register_blueprint(crop_planning_bp, url_prefix='/crop_planning')


    return application
