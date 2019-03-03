from flask_script import Command

class AddCrops(Command):
    def run(self):
        print('Importing db and Crop')
        from solarvibes import create_app, db
        from solarvibes.models import Crop
        from solarvibes.utils.db_postgresql.crop_db import crops
        print('Creating App Context')
        app = create_app()
        with app.app_context():
            print('Starting to add crops to db')
            if not Crop.query.first():
                for crop in crops:
                    crop_to_db = Crop(**crops[crop])
                    db.session.add(crop_to_db)
                db.session.commit()
                print('Crops added to db! Done!')
            else:
                print('Crops already in db!')

class AddUsers(Command):
    def run(self):
        print('Importing db and User')
        from solarvibes import create_app, db
        from solarvibes.models import User
        from solarvibes.utils.db_postgresql.user_db import test_user
        print('Creating App Context')
        app = create_app()
        with app.app_context():
            print('Starting to add users to db')
            if not User.query.first():
                for user in test_user:
                    user_to_db = User(**test_user[user])
                    db.session.add(user_to_db)
                db.session.commit()
                print('Users added to db! Done!')
            else:
                print('Users already in db!')

class AddLicenses(Command):
    def run(self):
        ###############################################
        from collections import namedtuple
        Agridata = namedtuple('Agridata', 'type table')

        from solarvibes.models import AgrimoduleList, AgrisensorList, AgripumpList
        agmodule = Agridata(type='Agrimodule', table=AgrimoduleList)
        agsensor = Agridata(type='Agrisensor', table=AgrisensorList)
        agpump = Agridata(type='Agripump', table=AgripumpList)

        agsensors = [agmodule, agsensor, agpump]
        ###############################################
        print('Importing db and Licenses models')
        from solarvibes import create_app, db
        from solarvibes.models import AgrimoduleList, AgrisensorList, AgripumpList
        from solarvibes.utils.db_postgresql.iot_licenses_db import licenses
        ###############################################
        print('Creating App Context')
        app = create_app()
        with app.app_context():

            print('Starting to add licenses to db')
            for sensor in agsensors:
                if not sensor.table.query.first():
                    print(f'Adding {sensor.type} licenses')
                    for license in licenses[sensor.type]:
                        license_to_db = sensor.table(
                                            identifier = license,
                                            type = agmodule.type,
                                            has_user_registered = False,
                                            user_id = None,
                                            has_agrimodule_registered = False,
                                            )
                        db.session.add(license_to_db)
                    print(f'Added licenses to {sensor.table}')
                    db.session.commit()
                else:
                    print(f'Licenses at {sensor.table} already in db!')
            print('Done!')
