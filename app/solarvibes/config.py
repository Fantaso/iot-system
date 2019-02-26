from os import environ

class Config:

    ########## SERVER ##########
    # HOST = '192.168.1.17'
    # PORT = 8000
    DEBUG = True


    ########## GENERAL ##########
    SECRET_KEY = environ.get('SECRET_KEY')


    ########## FLASK-SECURITY ##########
    SECURITY_PASSWORD_HASH = environ.get('SECURITY_PASSWORD_HASH')
    # SECURITY_PASSWORD_HASH = 'plaintext' # when change later, SALT must be configure too.
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_REGISTERABLE = True 	# allows register form template from flask-security
    SECURITY_CONFIRMABLE = False	# users must confirm their email throught nthe liunk provided in the welcome email
    SECURITY_RECOVERABLE = True		# allows user to recover email or reset password when forgot
    SECURITY_CHANGEABLE = True 		# enable the change password
    # SECURITY_RETYPABLE = True 		# allows for typing pass 2 times for confirmation (DONT EXIST IN DOCUMENTAITION)
    SECURITY_TRACKABLE = True 		# allows server to track statistics about the user acount like lastlogin,currentip etc.
    SECURITY_SEND_REGISTER_EMAIL = False 	# to disable/enable sending a confirmation email for registering without configuring the email register yet.
    # SECURITY_EMAIL_SENDER = environ.get('MAIL_USERNAME')
    SECURITY_URL_PREFIX = '/auth'
    SECURITY_POST_LOGIN_VIEW = '/login-check'
    SECURITY_POST_LOGOUT_VIEW = '/auth/login'
    # SECURITY_BLUEPRINT_NAME = 'auth'
    # SECURITY_LOGOUT_URL = '/auth/logout'
    # SECURITY_LOGIN_URL = '/auth/login'
    # SECURITY_REGISTER_URL = '/auth/register'
    # SECURITY_RESET_URL = '/auth/reset_password'
    # SECURITY_CHANGE_URL = '/auth/change_password'


    ########## SQLALCHEMY ##########
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')



    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    ########## FLASK-MAIL ##########
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
