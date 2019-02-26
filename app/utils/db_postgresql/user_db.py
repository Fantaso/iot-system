from ass import db, User, Role
from datetime import date
from sqlalchemy.sql import func

users = { 	
			'carlos':
					{
					'name':'Carlos',
				    'last_name':'Rosas',
				    'email':'cmrhsv@gmail.com',
				    'password':'cmrhsv',
				    'birthday': date(1986, 2, 27),
				    'mobile':'+4917647645375',
				    'active':True,
    				'confirmed_at':None
					},
			'swathish': 
					{
					'name':'Swathish',
				    'last_name':'Ravi',
				    'email':'swathish.ravi@gmail.com',
				    'password':'swathish.ravi',
				    'birthday': date(1990, 5, 14),
				    'mobile':'+4917587878787',
				    'active':True,
    				'confirmed_at':None
					},
			'mansoor':
					{
					'name':'Mohgul',
				    'last_name':'Mansoor',
				    'email':'mohgul.mansoor@gmail.com',
				    'password':'mohgul.mansoor',
				    'birthday': date(1988, 12, 1),
				    'mobile':'+4917655252526',
				    'active':True,
    				'confirmed_at':None
					}, 
			'viktor':
					{
					'name':'Viktor',
				    'last_name':'Veeser',
				    'email':'viktor.veeser@gmail.com',
				    'password':'viktor.veeser',
				    'birthday': date(1989, 6, 22),
				    'mobile':'+4917545123695',
				    'active':True,
    				'confirmed_at':None
					},
			'pavarthi':
					{
					'name':'Pavarthi',
				    'last_name':'Radja',
				    'email':'pavarthi.radja@gmail.com',
				    'password':'pavarthi.radja',
				    'birthday': date(1982, 5, 17),
				    'mobile':'+491765848596',
				    'active':True,
    				'confirmed_at':None
					},
			'oscar':
					{
					'name':'Oscar',
				    'last_name':'Guerrero',
				    'email':'oscar.guerrero@gmail.com',
				    'password':'oscar.guerrero',
				    'birthday': date(1986, 9, 11),
				    'mobile':'+4917455668891',
				    'active':True,
    				'confirmed_at':None
					},
			'vera':
					{
					'name':'Vera',
				    'last_name':'Anna',
				    'email':'vera.anna@gmail.com',
				    'password':'vera.anna',
				    'birthday': date(1987, 11, 16),
				    'mobile':'+4917455668899',
				    'active':True,
    				'confirmed_at':None
					},
		}

# Automatically add users to the db through SQLAlchemy
def add_users(users):
	print('Starting inserting users to db')
	for user in users:
		user_to_db = User(**users[user])
		db.session.add(user_to_db)
	db.session.commit()
	print('Users added to db! Done!')


# TO ADD THESE CROP DATASETS RUN:
if __name__ == '__main__':
	add_users(users)