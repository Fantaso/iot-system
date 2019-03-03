from ass import db, User, AgrimoduleSystem

agrimodulesystems = {
			'agrimodulesystem1':
					{
					'_identifier_agrimodulesystem':'identifierkey_sys1',
					'_identifier_agrimodule':'identifierkey_sys1a',
					'_identifier_agripump':'identifierkey_sys1p',
					'_lat_agrimodule':50.5,
					'_lon_agrimodule':40.2,
					'_lat_agripump':50.6,
					'_lon_agripump':40.3,
				    },
			'agrimodulesystem2':
					{
					'_identifier_agrimodulesystem':'identifierkey_sys2',
					'_identifier_agrimodule':'identifierkey_sys2a',
					'_identifier_agripump':'identifierkey_sys2p',
					'_lat_agrimodule':50.5,
					'_lon_agrimodule':40.2,
					'_lat_agripump':50.6,
					'_lon_agripump':40.3,
				    },
			'agrimodulesystem3':
					{
					'_identifier_agrimodulesystem':'identifierkey_sys3',
					'_identifier_agrimodule':'identifierkey_sys3a',
					'_identifier_agripump':'identifierkey_sys3p',
					'_lat_agrimodule':50.5,
					'_lon_agrimodule':40.2,
					'_lat_agripump':50.6,
					'_lon_agripump':40.3,
				    },
			'agrimodulesystem4':
					{
					'_identifier_agrimodulesystem':'identifierkey_sys4',
					'_identifier_agrimodule':'identifierkey_sys4a',
					'_identifier_agripump':'identifierkey_sys4p',
					'_lat_agrimodule':50.5,
					'_lon_agrimodule':40.2,
					'_lat_agripump':50.6,
					'_lon_agripump':40.3,
				    },    	}

# brand = db.Column(db.String(25))
# flow_rate = db.Column(db.Float(precision=2), nullable=False)
# height_max = db.Column(db.Float(presicion=2), nullable=False)
# kwh = db.Column(db.Float(precision=2), nullable=False)


def get_user(user_name):
	user = User.query.filter_by(name=user_name).first()
	print('Got the user {}'.format(user.name))
	return user

# Automatically add crops to the db through SQLAlchemy
def add_agrimodulesystems(agrimodulesystems, user):
	print('Starting inserting agrimodulesystems to db to user: {}'.format(user))
	for agrimodulesystem in agrimodulesystems:
		agrimodulesystem_to_db = AgrimoduleSystem(**agrimodulesystems[agrimodulesystem], user=user)
		db.session.add(agrimodulesystem_to_db)
	db.session.commit()
	print('Agrimodulesystems added to db! Done!')


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
			add_agrimodulesystems(agrimodulesystems, u) # pumps come from the pump dictionary manual db'''

# TO ADD THESE CROP DATASETS RUN:

if __name__ == '__main__':
	u1 = get_user('Oscar')
	add_agrimodulesystems(agrimodulesystems, u1)