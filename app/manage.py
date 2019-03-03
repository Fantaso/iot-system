from flask_script import Server, Manager
from solarvibes import create_app
from flask_migrate import MigrateCommand

from solarvibes.utils.db_postgresql.manage_cmds import AddCrops, AddUsers


# manager
#################################
manager = Manager(create_app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port=5000))
manager.add_command('addcrops', AddCrops())
manager.add_command('addusers', AddUsers())




if __name__ == '__main__':
    manager.run()
