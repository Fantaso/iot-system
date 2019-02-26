from ass import db, Field, Farm, User, Crop
from datetime import datetime, timedelta


user1='Oscar'
user2='Carlos'

farm1='farm berlin'
farm2='farm tamil'
farm3='farm venezuela'
farm4='farm indonesia'

crop1='plum'
crop2='arugula'
crop3='romaine'
crop4='radicchio'

field1='field of plums'
field2='field of arugulas'
field3='field of romaines'
field4='field of radicchios'

# FOLLOW THIS PATH AND CREATE A FIELD FOR AN SPECIFIC FARM AND CROP
# osci = User.query.filter_by(name='Oscar').first()
# farm_osci = osci.farms.filter_by(name = 'farm berlin').first()
# crop1 = Crop.query.filter_by(_name = 'plum').first()
# field1 = Field(name='plumming',size=500, date_start=datetime(2018,4,25), date_finish=datetime(2018,5,20), _current_yield=50.333, farm=farm_osci)
# field1.crops.append(crop1)


fields = {
			field1:
					{
					'name': field1,
				    'size':500,
				    'date_start': datetime(2018, 4, 25),
				    'date_finish': ( datetime(2018, 4, 25) + timedelta(Crop.query.filter_by(_name = crop1).first()._dtg + Crop.query.filter_by(_name = crop1).first()._dtm) ),
				    '_current_yield':
				    				(Crop.query.filter_by(_name = crop1).first()._yield \
				    					* (500 / Crop.query.filter_by(_name = crop1).first()._density) ),
				    },
			field2:
					{
					'name': field2,
				    'size':200,
				    'date_start': datetime(2018, 4, 25),
				    'date_finish': ( datetime(2018, 4, 25) + timedelta(Crop.query.filter_by(_name = crop2).first()._dtg + Crop.query.filter_by(_name = crop2).first()._dtm) ),
				    '_current_yield':
				    				(Crop.query.filter_by(_name = crop2).first()._yield \
				    					* (500 / Crop.query.filter_by(_name = crop2).first()._density) ),
				    },
			field3:
					{
					'name': field3,
				    'size':200,
				    'date_start': datetime(2018, 4, 25),
				    'date_finish': ( datetime(2018, 4, 25) + timedelta(Crop.query.filter_by(_name = crop3).first()._dtg + Crop.query.filter_by(_name = crop3).first()._dtm) ),
				    '_current_yield':
				    				(Crop.query.filter_by(_name = crop3).first()._yield \
				    					* (500 / Crop.query.filter_by(_name = crop3).first()._density) ),
				    },
			field4:
					{
					'name': field4,
				    'size':100,
				    'date_start': datetime(2018, 4, 25),
				    'date_finish': ( datetime(2018, 4, 25) + timedelta(Crop.query.filter_by(_name = crop1).first()._dtg + Crop.query.filter_by(_name = crop1).first()._dtm) ),
				    '_current_yield':
				    				(Crop.query.filter_by(_name = crop1).first()._yield \
				    					* (500 / Crop.query.filter_by(_name = crop1).first()._density) ),
				    },
    	}


# Automatically add fields to the db through SQLAlchemy
# Notes:
#		Currentl_yield is not done automatically, but nany how.. this is how extacly you can add data to a field with a many to many relationship
# 		stills needs to know how to erase a many to many relationship form db. you must erase the table association first.
def add_field(fields, user_name, farm_name, field_name, crop_name):
	user = User.query.filter_by(name = user_name).first()
	farm = user.farms.filter_by(name = farm_name).first()
	crop = Crop.query.filter_by(_name = crop_name).first() # It will always add plum unless told so later on.
	print( "Adding {2} to {0}'s {1} to cultivate {3}".format(user.name, farm.name, field_name, crop._name) )
	field_to_db = Field(**fields[field_name], farm=farm) # create the field object
	field_to_db.crops.append(crop) # add the crop to the field object
	db.session.add(field_to_db)
	db.session.commit()
	print('Field added to db!')


if __name__ == '__main__':
	add_fields()