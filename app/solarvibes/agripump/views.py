from flask import Blueprint, render_template, redirect, url_for, flash
from solarvibes.models import User, Agripump, Agrimodule, Field
from flask_login import current_user
from flask_security import login_required

agripump_bp = Blueprint(
    'agripump_bp',
    __name__,
    template_folder="templates"
)


##################
# USER AGRIPUMP
##################
@agripump_bp.route('/', methods=['GET'])
@agripump_bp.route('/<agripump_id>', methods=['GET'])
@login_required
def show(agripump_id = None):

    # Validation
    if agripump_id == None:
        flash('page not allowed')
        return redirect(url_for('main.index'))

    if Agripump.query.filter_by(id=agripump_id).first() == None:
        flash('That agripump do NOT exist')
        return redirect(url_for('main.index'))

    # objects query
    user = current_user
    agripump = Agripump.query.filter_by(id = agripump_id).first()
    agrimodule = Agrimodule.query.filter_by(id = agripump.agrimodule_id).first()
    field = Field.query.filter_by(id = agrimodule.field_id).first()
    farm = user.farms.filter_by(id = field.farm_id).first()
    crop = field.crops.first()


    pump = user.pumps.filter_by(id = agripump.pump_id).first()
    print(user)
    print(farm)
    print(crop)
    print(pump)
    print(agripump)

    # calculating pump information
    def mlpm_to_lps(mlpm):
        return mlpm / (1000 * 60)
    def cm_to_m(cm):
        return cm / 100
    def w_to_kw(w):
        return w / 1000
    pump_info = {'pump_name': pump.pump_name, 'pump_brand': pump.pump_brand, 'pump_flow_rate':mlpm_to_lps(pump.pump_flow_rate), 'pump_watts':w_to_kw(pump.pump_watts), 'pump_head':cm_to_m(pump.pump_head)}

    # Calculating energy consumption full cycle
    def w_to_wm(w):
        return w * 60
    def wm_to_kwh(wm):
        return wm / (60 * 60 * 1000)

    pump_Wmin_consumption = w_to_wm(pump.pump_watts)
    pump_minutes_on = field.field_water_required_day / pump.pump_flow_rate
    pump_Wmin_conmsumption_on = pump_Wmin_consumption * pump_minutes_on
    pump_consumption_kwh_per_day = wm_to_kwh(pump_Wmin_conmsumption_on)
    # pump_consumption = {'' : , '' : , '' : , '' : , '' : , '' : , }

    return render_template('agripump/show.html',
                            pump = pump_info,
                            agripump = agripump,
                            farm = farm,
                            field = field,
                            crop = crop,
                            pump_consumption_kwh_per_day=pump_consumption_kwh_per_day,
                            sensortype = 'Agripump',
                            system_name = agrimodule.name)





# AGRIPUMP
# TIME USAGE
# start_hour_per_day = db.Column(db.Integer)
# qty_hour_per_day = db.Column(db.Integer)

# time_per_hour = db.Column(db.Float)
# time_per_day = db.Column(db.Float)
# time_per_cycle = db.Column(db.Float)
# WATER USAGE
# water_per_hour = db.Column(db.Integer)
# water_per_day = db.Column(db.Integer)
# water_per_cycle = db.Column(db.Integer)
# ENERGY USAGE
# energy_per_hour = db.Column(db.Integer)
# energy_per_day = db.Column(db.Integer)
# energy_per_cycle = db.Column(db.Integer)

# PUMP
# brand = db.Column(db.String(25))
# flow_rate = db.Column(db.Float(precision=2), nullable=False)
# height_max = db.Column(db.Float(presicion=2), nullable=False)
# wh = db.Column(db.Float(precision=2), nullable=False)
