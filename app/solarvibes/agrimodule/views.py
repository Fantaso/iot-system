from flask import Blueprint, render_template, redirect, url_for, flash
from solarvibes.models import User, Agrimodule, Measurement, Agrisensor, Field
from flask_login import current_user
from flask_security import login_required

agrimodule_bp = Blueprint(
    'agrimodule_bp',
    __name__,
    template_folder="templates"
)


##################
# USER SHOW AGRIMODULE
##################
@agrimodule_bp.route('/', methods=['GET'])
@agrimodule_bp.route('/<agrimodule_id>', methods=['GET'])
@login_required
def show_agrimodule(agrimodule_id = None):

    if agrimodule_id == None:
        flash('page not allowed')
        return redirect(url_for(main.index))

    if Agrimodule.query.filter_by(id=agrimodule_id).first() == None:
        flash('That agrimodule do NOT exist')
        return redirect(url_for(main.index))

    user = current_user
    agrimodule = current_user.agrimodules.filter_by(id = agrimodule_id).first()
    # TODO: better filter the farm and field and the crop that is being passed to render in MAIN and AGRIMODULE blueprint with agrisensor in agrimodule blueprint also checked

    # TODO: here is for only 1 crop in the field. but when mix cultivation or multi. need to reflect more than 1 crop
    field = Field.query.filter_by(id = agrimodule.field_id).first()
    farm = user.farms.filter_by(id = field.farm_id).first()
    system_name = agrimodule.name
    crop = field.crops.first()
    measurement = agrimodule.measurements.order_by(Measurement.timestamp.desc()).first()

    return render_template('agrimodule/show.html', sensor_id = agrimodule_id, sensor = agrimodule, measurement = measurement, crop = crop, farm = farm, field = field, sensortype = 'Agrimodule', system_name = system_name)

##################
# USER SHOW AGRISENSOR
##################
@agrimodule_bp.route('/<agrimodule_id>/agrisensor', methods=['GET'])
@agrimodule_bp.route('/<agrimodule_id>/agrisensor/<agrisensor_id>', methods=['GET'])
@login_required
def show_agrisensor(agrimodule_id = None, agrisensor_id = None):

    if Agrimodule.query.filter_by(id=agrimodule_id).first() == None:
        flash('That agrimodule do NOT exist')
        return redirect(url_for(main.index))
    if Agrisensor.query.filter_by(id=agrisensor_id).first() == None:
        flash('That agrisensor do NOT exist')
        return redirect(url_for(main.index))

    if agrimodule_id == None:
        flash('page not allowed')
        return redirect(url_for(main.index))
    if agrisensor_id == None:
        flash('pag not allowed')
        return redirect(url_for(main.index))

    user = current_user
    agrimodule = current_user.agrimodules.filter_by(id = agrimodule_id).first()
    agrisensor = agrimodule.agrisensors.filter_by(id = agrisensor_id).first()
    field = Field.query.filter_by(id = agrimodule.field_id).first()
    farm = user.farms.filter_by(id = field.farm_id).first()
    system_name = agrimodule.name
    crop = field.crops.first()
    measurement = agrimodule.measurements.order_by(Measurement.timestamp.desc()).first()

    return render_template('agrimodule/show.html', sensor_id = agrisensor_id, sensor = agrisensor, measurement = measurement, crop = crop, farm = farm, field = field, sensortype = 'Agrisensor', system_name = system_name)


# print (crop._soil_ph_min)
# print (crop._soil_ph_max)
# print (crop._soil_temp_min)
# print (crop._soil_temp_max)
# print (crop._soil_humi_min)
# print (crop._soil_humi_max)
# print (crop._soil_nutrient_min)
# print (crop._soil_nutrient_max)
# print (crop._air_temp_min)
# print (crop._air_temp_max)
# print (crop._air_humi_min)
# print (crop._air_humi_max)

# print(ag_measurement.timestamp)
# print(ag_measurement.soil_ph)
# print(ag_measurement.soil_nutrient)
# print(ag_measurement.soil_temp)
# print(ag_measurement.soil_humi)
# print(ag_measurement.air_temp)
# print(ag_measurement.air_humi)
# print(ag_measurement.air_pres)
# print(ag_measurement.solar_radiation)
# print(ag_measurement.batt_status)
# print(ag_measurement.lat)
# print(ag_measurement.lon)
