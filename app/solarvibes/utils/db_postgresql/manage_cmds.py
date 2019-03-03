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
