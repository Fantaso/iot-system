from flask_script import Server, Manager
from solarvibes import create_app
from flask_migrate import MigrateCommand


# manager
#################################
manager = Manager(create_app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port=5000))


if __name__ == '__main__':
    manager.run()
