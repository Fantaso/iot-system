from datetime import datetime, timezone

def add_measurements(measurements, agrimodule_id):
	print('Importing db and Agrimodule')
	from solarvibes import db
	from solarvibes.models import Measurement
	from datetime import datetime, timezone
	print('Starting inserting measurements to db')
	for measurement in measurements:
		measurement_to_db = Measurement(**measurements[measurement], agrimodule_id=agrimodule_id)
		db.session.add(measurement_to_db)
	db.session.commit()
	print('Measurements added to db! Done!')


measurements = {
			'first':
					{
					'timestamp':datetime.now(timezone.utc),
					'soil_ph':6.58,
				 	'soil_nutrient':68.25,
					'soil_temp':23.4, #
					'soil_humi':45, #
					'air_temp':28.9, #
					'air_humi':62.3, # ``
					'air_pres':8.2, #
					'solar_radiation':325,
					'batt_status':95, #
					'lat':52.25, #
					'lon':18.23, #
					},
			'second':
					{
					'timestamp':datetime.now(timezone.utc),
					'soil_ph':5.58,
				 	'soil_nutrient':88.25,
					'soil_temp':21.4, #
					'soil_humi':32, #
					'air_temp':25.9, #
					'air_humi':85.3, # ``
					'air_pres':15.2, #
					'solar_radiation':750,
					'batt_status':35, #
					'lat':8.25, #
					'lon':28.23, #
					},
		}
