from ass import db, User, Pump
from random import randint

pumps = {
			'pump1':
					{
					'brand':'ITT',
				    'flow_rate':50.00,
				    'height_max':10.00,
				    'kwh':250.00,
				    },
			'pump2':
					{
					'brand':'Ebara',
				    'flow_rate':60.00,
				    'height_max':10.00,
				    'kwh':300.00,
				    },
			'pump3':
					{
					'brand':'Grundfos',
				    'flow_rate':80.00,
				    'height_max':15.00,
				    'kwh':350.00,
				    },
			'pump4':
					{
					'brand':'Flowserve',
				    'flow_rate':120.00,
				    'height_max':20.00,
				    'kwh':500.00,
				    },
    	}

# brand = db.Column(db.String(25))
# flow_rate = db.Column(db.Float(precision=2), nullable=False)
# height_max = db.Column(db.Float(presicion=2), nullable=False)
# kwh = db.Column(db.Float(precision=2), nullable=False)


def get_user(user_name):
	user = User.query.filter_by(name=user_name).first()
	print('Got the user {}'.format(user.name))
	return user

# Automatically add crops to the db through SQLAlchemy
def add_pumps(pumps, user):
	print('Starting inserting pump to db to user: {}'.format(user))
	for pump in pumps:
		pump_to_db = Pump(**pumps[pump], user=user)
		db.session.add(pump_to_db)
	db.session.commit()
	print('Pumps added to db! Done!')


# due to db.session not handle in the app yet.  different methods cant be used to add automatically to the db.
# USE the random_user to the the user in a python repl session and then pass in the same session the random_user to add the farms
'''e.g.
		u1 = get_user('Oscar')
		u2 = get_user()
		u3 = get_user()
		u4 = get_user()
		u5 = get_user()
		u6 = get_user()
		u7 = get_user()
		us = [u1, u2, u3, u4, u5, u6, u7]
		for u in us:
			add_pumps(pumps, u) # pumps come from the pump dictionary manual db'''

# TO ADD THESE CROP DATASETS RUN:

if __name__ == '__main__':
	u1 = get_user('Oscar')
	add_pumps(pumps, u1)