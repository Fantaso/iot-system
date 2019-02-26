import os
from datetime import datetime, timedelta, timezone, time

class CropData():

    """this class contains the CropData  information and its callable
    methods to retrieve all information regarding its:
    1. CROP CHARATERISTICS
    2. CROP IRRIGATION SCHEDULE
    3. CROP FERTILIZATION SCHEDULE"""


    __CROP_IMAGES_FOLDER_NAME = 'crop_images'
    __CROPS = {
    	'green_cardamom': {
    		'characteristics': {
    			'name':'green_cardamom',
    			'variety':'cardamom',
    		 	'family':'dry fruit',
    			'image': CropData.get_rel_path(filename = 'green_cardamom.png', image_folder = __CROP_IMAGES_FOLDER_NAME),
    			'yield': 122.1153, # gr
    			'canopy_x':0.9, # m
    			'canopy_y':0.9, # m
    			'canopy_z':3, # m height
    			'density':2500, # plants/hectare
    			'fruit_quantity':610.5765,
    			'fruit_size':7.6, # mm
    			'fruit_weight':0.2, # gr
    			'root_depth':45, # cm
    			'lifecycle': 'perenial',
    			'recommended_sowing_start': datetime(1,9,1), # september
    			'recommended_transplant_start': datetime(1,6,1), # june
    		},
    		'growth_stages': {
    			'in_nursery': {
    				'sow': 1, # week
    				'germination': 33, # week
    			},
    			'in_field': {
    			 	'transplant': 1, # week
    				'vegetative_growth': 76, # week
    				'flowering': 8, # week
    				'fruit_development': 8, # week
    				'maturity': 12, # week
    				'harvest':4, # week
    			},
    		},
    		'soil_characteristics': {
    			'soil': {
    			 	'preferences': 'loamy forest soils', #
    			},
    			'temperature': {
    			 	'min': 10, # celcius
    				'opt': 18, #
    				'max': 35, #
    			},
    			'moisture': {
    			 	'min': 45, # % moisture
    				'opt': 48, #
    				'max': 50, #
    			},
    			'ph': {
    			 	'min': 4.5, # potential hydrogen - acidicity /alkaline
    				'opt': 6.5, #
    				'max': 7, #
    			},
    			'ec': {
    			 	'min': 0, # electrical conductivity - salinity
    				'opt': 0, #
    				'max': 0, #
    			},
    		},
    		'weather_characteristics': {
    			'weather': {
    			 	'preferences': 'forest weather, humid, normally grown under other bigger crops', #
    			},
    			'temperature': {
    			 	'min': 10, # celcius
    				'opt': 18, #
    				'max': 35, #
    			},
    			'humidity': {
    			 	'min': 60, # % relative humidity
    				'opt': None, #
    				'max': 75, #
    			},
    			'light': {
    			 	'min': 8, # amount of light hours or solar radiation
    				'opt': None, #
    				'max': 12, #
    			},
    			'radiation': {
    			 	'min': None, # watts/m2 or MJoules/day etc amount of light hours or solar radiation
    				'opt': None, #
    				'max': None, #
    			},
    		},
    		'crop_patterns': {
    			'general': {
    			 	'layout': 'east-west', # directions of plantations
    				'layout_degree': 90, # degrees tor directions of layout
    			},
    			'seeding': {
     			 	'location': 'nursery', #
     				'seed_quantity': 40, # gr / bed
    				'bed_characteristics': {
        			 	'height': 0.2, # m
        				'width': 1, # m
       					'length': 6, # m
        			},
    				'planting_space': {
        			 	'plant_space': 0., # m
        				'row_space': 0.1, # m
        			},
     			},
    			'monoculture': {
    			 	'single_row': {
    				 	'plant_distance': 2, # m
    					'row_distance': 2, # m
    				},
    			},
    		},
    		'irrigation': {
    			'general': {
    				'recommended_time_start': time(8), # hour, min, sec
    				'recommended_time_finish': time(10), # hour, min, sec
    			},
    			'pot_irrigation': {
    				'in_nursery': {
    					'sow': {
    						'water': 2, # liters / bed
    						'frequency': 1, # every 1
    					},
    					'germination': {
    						'water': 2, # liters / bed
    						'frequency': 14, # every 1
    					},
    				},
    				'in_field': {
    				 	'transplant': {
    						'water': 4.28, # liters / bed
    						'frequency': 14, # every 1
    					},
    					'vegetative_growth': {
    						'water': 4.28, # liters / bed
    						'frequency': 14, # every 1
    					},
    					'flowering': {
    						'water': 4.28, # liters / bed
    						'frequency': 14, # every 1
    					},
    					'fruit_development': {
    						'water': 4.28, # liters / bed
    						'frequency': 14, # every 1
    					},
    					'maturity': {
    						'water': None, # liters / bed
    						'frequency': None, # every 1
    					},
    					'harvest':{
    						'water': None, # liters / bed
    						'frequency': None, # every 1
    					},
    				},
    			},
    			'sprinkler_irrigation': {
    				'in_nursery': {
    					'sow': {
    						'water': 2, # liters / bed
    						'frequency': 1, # every 1
    					},
    					'germination': {
    						'water': 2, # liters / bed
    						'frequency': 14, # every 1
    					},
    				},
    				'in_field': {
    				 	'transplant': {
    						'water': 40, # liters / bed
    						'frequency': 14, # every 1
    					},
    					'vegetative_growth': {
    						'water': 40, # liters / bed
    						'frequency': 14, # every 1
    					},
    					'flowering': {
    						'water': 40, # liters / bed
    						'frequency': 14, # every 1
    					},
    					'fruit_development': {
    						'water': 40, # liters / bed
    						'frequency': 14, # every 1
    					},
    					'maturity': {
    						'water': None, # liters / bed
    						'frequency': None, # every 1
    					},
    					'harvest':{
    						'water': None, # liters / bed
    						'frequency': None, # every 1
    					},
    				},
    			},
    			'drip_irrigation': {
    				'in_nursery': {
    					'sow': {
    						'water': 2, # liters / bed
    						'frequency': 1, # every 1
    					},
    					'germination': {
    						'water': 2, # liters / bed
    						'frequency': 14, # every 1
    					},
    				},
    				'in_field': {
    				 	'transplant': {
    						'water': 5, # liters / bed
    						'frequency': 14, # every 1
    					},
    					'vegetative_growth': {
    						'water': 5, # liters / bed
    						'frequency': 14, # every 1
    					},
    					'flowering': {
    						'water': 5, # liters / bed
    						'frequency': 14, # every 1
    					},
    					'fruit_development': {
    						'water': 5, # liters / bed
    						'frequency': 14, # every 1
    					},
    					'maturity': {
    						'water': None, # liters / bed
    						'frequency': None, # every 1
    					},
    					'harvest':{
    						'water': None, # liters / bed
    						'frequency': None, # every 1
    					},
    				},
    			},
            },
    		'fertilization': {
    			'transplant': {
    				'week': 7, # time of fert as the number of the week
    				'N': 12.5, # kg / hectare
    				'P2O5': 12.5, # kg / hectare
    				'N2O': 25, # kg / hectare
    			},
    			'vegetative_growth': {
    				'week': 8, # time of fert as the number of the week
    				'N': 12.5, # kg / hectare
    				'P2O5': 12.5, # kg / hectare
    				'N2O': 25, # kg / hectare
    			},
    			'flowering': {
    				'week': 7, # time of fert as the number of the week
    				'N': 12.5, # kg / hectare
    				'P2O5': 12.5, # kg / hectare
    				'N2O': 25, # kg / hectare
    			},
    			'fruit_development': {
    				'week': 7, # time of fert as the number of the week
    				'N': 12.5, # kg / hectare
    				'P2O5': 12.5, # kg / hectare
    				'N2O': 25, # kg / hectare
    			},
    			'maturity': {
    				'week': 7, # time of fert as the number of the week
    				'N': 12.5, # kg / hectare
    				'P2O5': 12.5, # kg / hectare
    				'N2O': 25, # kg / hectare
    			},
    			'harvest':{
    				'week': 7, # time of fert as the number of the week
    				'N': 12.5, # kg / hectare
    				'P2O5': 12.5, # kg / hectare
    				'N2O': 25, # kg / hectare
    			},
    		},
    	},
    }

    #########     INTERNAL METHODS     ##########

    def __init__(self, crop_name = None):

        """"this method initiates the crop variables to know
        which crop is the one that needs to get the calculations"""

        self.crop_name = crop_name
        self.images_folder_name = CropData.__CROP_IMAGES_FOLDER_NAME
        self.db = self.get_db()
        self.list = self.get_list()
        self.crop = self.get_crop()


    def __repr__(self):
        """"this method returns the object representation of this class"""
        return "{}({})".format(self.__class__.__name__, self.crop_name)


    def get_db(self):
    	""""this method returns the full dictionary of all crops and any information
        regarding crop chratacteristics, irrigation and fertilization schedule"""
    	return CropData.__CROPS

    #########     SET METHODS     ##########

    def set_crop_name(self, crop_name):
        self.crop_name = crop_name
        return 'your crop name is: {}'.format(self.crop_name)


    #########     GET METHODS     ##########

    def get_list(self):
        """"this method returns the full dictionary of all crops and any information
        regarding crop chratacteristics, irrigation and fertilization schedule"""
        crop_list = []
        for crop in CropData.__CROPS:
            crop_list.append(crop)
        return crop_list


    def get_crop(self):
        """"this method returns the full dictionary data of the specific crop created
        with this class"""
        if self.crop_name:
            return CropData.__CROPS[self.crop_name]
        else:
            return 'This crop instance hasnot been created. you can with instance.set_crop_name("green_cardamom")'


    def get_characteristics(self):
        """"this method returns the dictionary containing the specific crop
        characteristics"""
        return CropData.__CROPS[self.crop_name]['characteristics']


    def get_growth_stages(self):
        """"this method returns the dictionary containing the specific crop
        growth stages"""
        return CropData.__CROPS[self.crop_name]['growth_stages']


    def get_soil_characteristics(self):
        """"this method returns the dictionary containing the specific crop
        soil characteristics"""
        return CropData.__CROPS[self.crop_name]['soil_characteristics']


    def get_weather_characteristics(self):
        """"this method returns the dictionary containing the specific crop
        weather characteristics"""
        return CropData.CROPS[self.crop_name]['weather_characteristics']


    def get_crop_patterns(self):
        """"this method returns the dictionary containing the specific crop
        crop patterns"""
        return CropData.__CROPS[self.crop_name]['crop_patterns']


    def get_irrigation(self):
        """"this method returns the dictionary containing the specific crop
        irrigation schedule"""
        return CropData.__CROPS[self.crop_name]['irrigation']


    def get_fertilization(self):
        """"this method returns the dictionary containing the specific crop
        fertilization schedule"""
        return CropData.__CROPS[self.crop_name]['fertilization']


    #########     STATIC METHODS     ##########

    @static_method
    def get_rel_path(filename, image_folder):

        """"this method gets the relative path of the object and join
		the relative path and the filename for the crop images url
        to be access by the app to render pictures in the web app"""

        dirname = os.path.dirname(__file__)
        url = os.path.join(dirname, image_folder, filename)
        return url
