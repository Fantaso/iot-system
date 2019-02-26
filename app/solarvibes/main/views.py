from flask import Blueprint, render_template
from solarvibes.models import Field, Pump
from flask_login import current_user
from flask_security import login_required
from datetime import datetime, timezone


main = Blueprint(
    'main',
    __name__,
    template_folder="templates"
)


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    default_farm = current_user.farms.filter_by(_default = True).one()
    fields = Field.query.filter_by(farm_id = default_farm.id).all()
    pump_db = Pump.query
    return render_template('main/index.html',
                                user=current_user,
                                default_farm = default_farm,
                                fields = fields,
                                pump_db =pump_db,
                                timenow=datetime.now(timezone.utc))
