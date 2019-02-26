from ass import db, Farm, User
from random import randint

farms = {
			'farm berlin':
					{
					'name':'farm berlin',
				    'location':'berlin',
				    'size':1000.00,
				    'user_id':'',
				    'fields':'',
				    },
			'farm tamil':
					{
					'name':'farm tamil',
				    'location':'tamil',
				    'size':800.00,
				    'user_id':'',
				    'fields':'',
				    },
			'farm venezuela':
					{
					'name':'farm venezuela',
				    'location':'venezuela',
				    'size':3000.00,
				    'user_id':'',
				    'fields':'',
				    },
			'farm indonesia':
					{
					'name':'farm indonesia',
				    'location':'indonesia',
				    'size':500.00,
				    'user_id':'',
				    'fields':'',
				    },
    	}

def get_user():
	random_user = User.query.filter_by(id=randint(1,7)).first()
	print('Got the user!')
	return random_user

# Automatically add crops to the db through SQLAlchemy
def add_farms(farms, random_user):
	print('Starting inserting farms to db to user: {}'.format(random_user))
	for farm in farms:
		farm_to_db = Farm(**farms[farm], user=random_user)
		db.session.add(farm_to_db)
	db.session.commit()
	print('Farms added to db! Done!')


# due to db.session not handle in the app yet.  different methods cant be used to add automatically to the db.
# USE the random_user to the the user in a python repl session and then pass in the same session the random_user to add the farms
'''e.g.
		ru1 = get_user()
		ru2 = get_user()
		ru3 = get_user()
		ru4 = get_user()
		ru5 = get_user()
		ru6 = get_user()
		ru7 = get_user()
		rus = [ru1, ru2, ru3, ru4, ru5, ru6, ru7]
		for ru in rus:
			add_farms(farms, ru) # farms come from the farm dictionary manual db'''

def add_farm_with_user(farms):
	random_user = get_user()
	add_farms(farms, random_user)
# TO ADD THESE CROP DATASETS RUN:

if __name__ == '__main__':
	add_farms()