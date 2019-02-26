from flask import Blueprint, render_template
from solarvibes.models import Farm, Field, Pump, Agripump
from flask_login import current_user
from flask_security import login_required
from datetime import datetime, timezone

settings = Blueprint(
    'settings',
    __name__,
    template_folder="templates"
)


##################
# USER FARMS
##################
@settings.route('/', methods=['GET'])
@login_required
def index():

    # USER FARMS
    user = current_user
    farms = user.farms.all()

    def progress():
        for farm in farms:
            # print(farm)
            for field in farm.fields.all():
                # print(field)
                for crop in field.crops.all():
                    # print(crop)
                    cycle_days_so_far = ( datetime.now(timezone.utc) - field.field_cultivation_start_date ).days
                    cycle_days = crop._dtm + crop._dtg
                    progress = (cycle_days_so_far / cycle_days) * 100
                    # print (cycle_days_so_far, cycle_days, progress)

    progress()
    timenow = datetime.now(timezone.utc)

    # USER AGRIMODULES
    user = current_user
    agrimodules = user.agrimodules.all()

    # def list_agrimodules():
        # for agrimodule in agrimodules:
            # print(agrimodule, agrimodule.identifier)
            # for agripump in agrimodule.agripumps.all():
                # print(agripump, agripump.identifier)
            # for agrisensor in agrimodule.agrisensors.all():
                # print(agrisensor, agrisensor.identifier)

    # list_agrimodules()
    # USER PUMPS
    pumps = user.pumps.all()

    farm_db = Farm.query
    field_db = Field.query
    pump_db = Pump.query
    agripump_db = Agripump.query

    return render_template('settings/index.html', farms = farms, timenow = timenow, agrimodules=agrimodules, farm_db = farm_db, field_db = field_db, pump_db = pump_db, pumps=pumps, agripump_db = agripump_db)
