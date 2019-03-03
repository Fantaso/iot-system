# Automatically add crops to the db through SQLAlchemy
# in run.py directory
# 				from utils.db.crop_db import

class CropApi():


	"""this class contains the API for managing and getting usefull
	resources from the CropData() class such as:
	1. yield predictions
	2. resources usage prediction"""

	def __init__(self, crop_name):
		""""this method initiates the crop variables to know
		which crop is the one that needs to get the calculations"""

		self.crop_name = crop_name

	def __repr__(self):
		""""this method returns the object representation of this class"""

		return "{}({})".format(self.__class__.__name__, self.crop_name)


	def add_crops(crops):
		""""this method will be used to add all the crops in here to the
		when and if created in localhost"""

		#  //TODO: the imports must be changed
		print('Importing db and Crop')
		from solarvibes import db
		from solarvibes.models import Crop
		print('Starting inserting crops to db')
		for crop in crops:
			crop_to_db = Crop(**crops[crop])
			db.session.add(crop_to_db)
		db.session.commit()
		print('Crops added to db! Done!')













# TO ADD THESE CROP DATASETS RUN:
# if __name__ == '__main__':
# 	add_crops(crops)
