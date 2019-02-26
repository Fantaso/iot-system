from flask import Blueprint, render_template, redirect, url_for, flash
from solarvibes.models import User, Field, Farm, Agrimodule
from flask_login import current_user
from flask_security import login_required
from datetime import datetime, timezone

crop_status = Blueprint(
    'crop_status',
    __name__,
    template_folder="templates"
)


##################
# USER CROP STATUS
##################
@crop_status.route('/', methods=['GET'])
@crop_status.route('/<field_id>', methods=['GET'])
@login_required
def show(field_id = None):

    # validation
    if field_id == None:
        flash('page not allowed')
        return redirect(url_for('main.index'))

    if Field.query.filter_by(id=field_id).first() == None:
        flash('That agrimodule do NOT exist')
        return redirect(url_for('main.index'))

    def cm2_to_m2(cm2):
            return cm2 / 10000

    def m2_to_cm2(m2):
            return m2 * 10000

    # db objects
    user = current_user
    field = Field.query.filter_by(id = field_id).first()
    agrimodule = Agrimodule.query.filter_by(field_id = field.id).first()
    farm = Farm.query.filter_by(id = field.farm_id).first()
    # TODO: here is for only 1 crop in the field. but when mix cultivation or multi. need to reflect more than 1 crop
    crop = field.crops.first()

    cycle_days_so_far = ( datetime.now(timezone.utc) - field.field_cultivation_start_date ).days
    today = datetime.now(timezone.utc)

    time_bar_percentage = (cycle_days_so_far * 100) / (crop._dtm + crop._dtg)
    yield_bar_percentage = (field.field_current_yield * 100) / (field.field_projected_yield)

    return render_template('crop_status/show.html',
                                crop = crop,
                                farm = farm,
                                field = field,
                                today = today,
                                cycle_days_so_far = cycle_days_so_far,
                                time_bar_percentage = time_bar_percentage,
                                yield_bar_percentage = yield_bar_percentage,
                                system_name = agrimodule.name)


##################
# USER CROP STATUS
##################
@crop_status.route('/show-all', methods=['GET'])
@login_required
def show_all():

    def cm2_to_m2(cm2):
            return cm2 / 10000

    def m2_to_cm2(m2):
            return m2 * 10000

    # db objects
    default_farm = current_user.farms.filter_by(_default = True).one()
    fields = default_farm.fields.all()

    # TODO: here is for only 1 crop in the field. but when mix cultivation or multi. need to reflect more than 1 crop
    # crop = field.crops.first()

    today = datetime.now(timezone.utc)
    # cycle_days_so_far = ( today - field.field_cultivation_start_date ).days


    # time_bar_percentage = (cycle_days_so_far * 100) / (crop._dtm + crop._dtg)
    # yield_bar_percentage = (field.field_current_yield * 100) / (field.field_projected_yield)

    return render_template('crop_status/show_all.html',
                                fields = fields,
                                today = today)
