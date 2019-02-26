from flask import Blueprint, render_template, redirect, url_for, flash
from solarvibes import db
from solarvibes.farm_settings.forms import FarmForm, FieldForm, PreNewCropForm, PreDateNewCropForm, NewCropForm, PreEditFarmForm, EditFarmForm
from solarvibes.models import User, Crop, Farm, Field, Agrimodule
from flask_login import current_user
from flask_security import login_required
from math import sqrt, floor
from datetime import datetime, timedelta

farm_settings = Blueprint(
    'farm_settings',
    __name__,
    template_folder="templates"
)

##################
# USER MAKE FARM DEFAULT
##################
@farm_settings.route('/default-farm', methods=['GET'])
@farm_settings.route('/default-farm/<farm_id>', methods=['GET'])
@login_required
def default_farm(farm_id = None):

    # TODO: can not erase default farm or assigned current erasing default farm to another farm
    if farm_id == None:
        flash('This page does not exist', _anchor = 'flash_msg')
        return redirect(url_for('settings.index'))

    # GET CURRENT DEFAULT FARM'S ID
    farm_default_old = current_user.farms.filter_by(_default = True).one()
    farm_default_old._default = False # ERASE THE DEFAULT LABEL
    # GET NEW DEFAULT FARM
    farm_default_new = current_user.farms.filter_by(id = farm_id).one()
    farm_default_new._default = True # ADD THE DEFAULT LABEL
    current_user.default_farm_id = farm_id # COPY FARM DEFAULT ID TO USER'S TABLE
    db.session.commit()

    flash('New default farm: {}'.format(farm_default_new.farm_name))
    return redirect(url_for('settings.index'))


##################
# USER FIELD
##################
# @farm_settings.route('/field', methods=['GET'])
# @login_required
# def user_field():
#     return render_template('field.html')

##################
# USER NEW FARM
##################
@farm_settings.route('/new-farm', methods=['GET', 'POST'])
@login_required
def new_farm():

    form = FarmForm()               # CREATE WTForm FORM
    if form.validate_on_submit():   # IF request.methiod == 'POST'
        def m2_to_cm2(m2):
            return m2 * 10000

        # USER OBJS
        user_id = current_user.get_id()

        # FARM OBJS
        farm_name = form.farm_name.data
        farm_location = form.farm_location.data
        farm_area = form.farm_area.data
        farm_cultivation_process = form.farm_cultivation_process.data

        # FARM OBJS  TO DB
        farm = Farm(    user_id=user_id,
                        farm_name=farm_name,
                        farm_location=farm_location,
                        farm_area=m2_to_cm2(farm_area),
                        farm_cultivation_process=farm_cultivation_process,
                        _default=False)

        # DB COMMANDS
        db.session.add(farm)
        db.session.commit()

        # SUCESS AND REDIRECT TO NEXT STEP
        flash('''You just created farm: {}
                    located: {}
                    with an area: {} m2
                    growing: {}ally'''.format(farm_name, farm_location, farm_area, farm_cultivation_process))
        return redirect(url_for('settings.index'))

    return render_template('farm_settings/new_farm.html', form=form)


##################
# USER EDIT FARM
##################

@farm_settings.route('/edit-farm', methods=['GET', 'POST'])
@farm_settings.route('/edit-farm/<farm_id>', methods=['GET', 'POST'])
@login_required
def edit_farm(farm_id = 0):

    try:
        # None should pass to this route without the farm ID
        if farm_id == 0:
            return redirect(url_for('main.index'))
        # INTERNAL METHODS
        def cm2_to_m2(cm2):
            return cm2 / 10000
        def m2_to_cm2(m2):
            return m2 * 10000

        farm = Farm.query.filter_by(id = farm_id).first()
        myFarm = PreEditFarmForm(   farm_name = farm.farm_name,
                                    farm_location = farm.farm_location,
                                    farm_area = cm2_to_m2(farm.farm_area),
                                    farm_cultivation_process = farm.farm_cultivation_process)

        form = EditFarmForm(obj=myFarm)
        if form.validate_on_submit():

            # VALIDATE FIELD AREA
            def validate_area():
                farm_area = m2_to_cm2(form.farm_area.data) # in cm2
                fields_in_farm = farm.fields.all()
                sum_areas = 0

                for each_field in fields_in_farm:
                    sum_areas += each_field.field_cultivation_area # in cm2
                result = farm_area - sum_areas

                if result < 0:
                    return False
                return True

            if not validate_area():
                flash('Your new farm area should not be smaller than the total land of all your fields in: {}'.format(farm.farm_name))
                return render_template('farm_settings/edit_farm.html', form=form, farm_id = farm.id)

            # SAVING FORM DATA IN SESSION OBJ
            farm.farm_name = form.farm_name.data
            farm.farm_location = form.farm_location.data
            farm.farm_area = m2_to_cm2(form.farm_area.data)
            farm.farm_cultivation_process = form.farm_cultivation_process.data

            # DB COMMANDS
            db.session.commit()

            flash('You just edited your farm: {}'.format(farm.farm_name))
            return redirect(url_for('settings.index'))


        return render_template('farm_settings/edit_farm.html', form=form, farm_id = farm_id)

    except Exception as e:
        flash('that farm doesnt exist' + str(e))
        return redirect(url_for('settings.index'))



##################
# USER DELETE FARM
##################
@farm_settings.route('/delete-farm/<farm_id>', methods=['GET'])
@login_required
def delete_farm(farm_id):

    # TODO: can not delete default farm or if can then erase the user tag 
    try:
        farm_to_del = Farm.query.filter_by(id = farm_id).first()
        fields_to_del_in_farm = farm_to_del.fields.all()
        for field in fields_to_del_in_farm:
            db.session.delete(field)
        db.session.delete(farm_to_del)
        db.session.commit()
        flash('You just deleted the farm: {}'.format(farm_to_del.farm_name))
        return redirect(url_for('settings.index'))
    except Exception as e:
        flash('Error: ' + str(e))
        db.session.rollback()
        return render_template('settings/index.html')
    else:
        pass
    finally:
        pass


    flash('Error in TRY')
    return render_template('settings/index.html')








##################
# USER NEW CROP
##################
@farm_settings.route('/new-crop', methods=['GET', 'POST'])
@farm_settings.route('/new-crop/<farm_id>', methods=['GET'])
@login_required
def new_crop(farm_id = None):

    # DYNAMIC FORM
    farm_choices = current_user.farms.all() # FARM CHOICE
    crop_choices = Crop.query.all() # CROP CHOICE


    today = datetime.now()
    in_a_week = today + timedelta(7)
    myDate = PreDateNewCropForm(field_cultivation_start_date = in_a_week)

    form = NewCropForm(obj = myDate)
    if farm_id == None:
        form.farm_choices.choices = [ (farm.id, farm.farm_name) for farm in farm_choices ] # FARM
        form.farm_choices.choices.insert(0, ('0' ,'Choose:'))
    else:
        farm = current_user.farms.filter_by(id = farm_id).first()
        form.farm_choices.choices = [ (farm.id, farm.farm_name) ] # FARM

    form.field_cultivation_crop.choices = [ (crop.id, str.capitalize(crop._name)) for crop in crop_choices ] # CROP
    form.field_cultivation_crop.choices.insert(0, ('0' ,'Choose:'))

    # POST REQUEST
    if form.validate_on_submit():

        # INTERNAL METHODS
        def cm2_to_m2(cm2):
            return cm2 / 10000

        def m2_to_cm2(m2):
            return m2 * 10000

        def num_plants():
            area_in_cm2 = m2_to_cm2(field_cultivation_area) # cm2
            distance_rows_and_columns = sqrt(area_in_cm2) # cm. since we receive an area instead of a shape, we assumed is perfect square
            num_of_rows = (floor(distance_rows_and_columns / crop._space_x))/2 #
            num_of_cols = (floor(distance_rows_and_columns / crop._space_y))/2 # since space of plant and space for walk is the same DIVIDE by 2
            num_of_plants = num_of_rows * num_of_cols
            return num_of_plants

        # USER OBJS
        user_id = current_user.get_id()
        user = User.query.filter_by(id = user_id).first()
        farm = user.farms.filter_by(id = form.farm_choices.data).first()

        # VALIDATE FIELD AREA
        def validate_area():
            farm_area = farm.farm_area # in cm2
            fields_in_farm = farm.fields.all()
            sum_areas = 0

            for each_field in fields_in_farm:
                sum_areas += each_field.field_cultivation_area # in cm2
            new_area = m2_to_cm2(form.field_cultivation_area.data) # in cm2

            result = farm_area - sum_areas - new_area

            if result < 0:
                return False
            return True

        if not validate_area():
            flash('Your new crop area should not exceed the available land on your farm: {}'.format(farm.farm_name))
            return render_template('farm_settings/new_crop.html', form=form)

        # Data from Form
        crop = Crop.query.filter_by(id = form.field_cultivation_crop.data).first()
        field_cultivation_area = form.field_cultivation_area.data # in m2
        field_cultivation_start_date = form.field_cultivation_start_date.data
        field_cultivation_state = form.field_cultivation_state.data
        field_cultivation_type = form.field_cultivation_type.data

        # Calculated vars
        field_cultivation_finish_date = field_cultivation_start_date + timedelta(crop._dtg + crop._dtm) # datetime
        field_num_plants = num_plants() # number Integer
        field_projected_yield = crop._yield * field_num_plants # gr
        field_current_yield = 0
        field_water_required_day = field_num_plants * crop._water

        # FIELD OBJS TO DB
        field = Field(  field_name=crop._name,
                        farm=farm,
                        field_cultivation_area=m2_to_cm2(field_cultivation_area),
                        field_cultivation_start_date=field_cultivation_start_date,
                        field_cultivation_state=field_cultivation_state,
                        field_cultivation_type=field_cultivation_type,
                        field_cultivation_finish_date = field_cultivation_finish_date,
                        field_current_yield = field_current_yield,
                        field_num_plants = field_num_plants,
                        field_water_required_day = field_water_required_day,
                        field_projected_yield = field_projected_yield)
        field.crops.append(crop)

        # DB COMMANDS
        db.session.add(field)
        db.session.commit()

        # DEAFULT AGRIMODULE SYSTEM
        if user.farms.count() == 1 and user.farms.first().fields.count() == 1 and user.agrimodules.count() > 0: # if first time and first field, set it as the default one
            print('Field default agrimodule system nummer {} was added and type {}'.format(field.id, type(field.id)))
            field.agrimodule = Agrimodule.query.first()
            db.session.commit()

        #SUCESS AND REDIRECT TO DASHBOARD
        flash('You just created a {} in your {}'.format(crop._name, farm.farm_name))
        return redirect(url_for('settings.index'))

    return render_template('farm_settings/new_crop.html', form=form)










##################
# USER EDIT CROP
##################
@farm_settings.route('/edit-crop/<field_id>', methods=['GET', 'POST'])
@login_required
def edit_crop(field_id):


    # INTERNAL METHODS
    def cm2_to_m2(cm2):
        return cm2 / 10000

    # get farm id from link
    # get field id from link


    field = Field.query.filter_by(id = field_id).first()
    print(field)
    # farm = current_user.farms.filter_by(id = 1).first()
    farm = Farm.query.filter_by(id = field.farm_id).first()
    print(farm)
    crop = field.crops.first()
    print(field.field_cultivation_start_date)

    myField = PreNewCropForm(field_cultivation_area = cm2_to_m2(field.field_cultivation_area),
                            field_cultivation_start_date = field.field_cultivation_start_date,
                            field_cultivation_state = field.field_cultivation_state,
                            field_cultivation_type = field.field_cultivation_type)

    form = NewCropForm(obj=myField)
    form.farm_choices.choices = [ (farm.id, farm.farm_name) ] # FARM
    form.field_cultivation_crop.choices = [ (crop.id, str.capitalize(crop._name)) ] # CROP

    # POST REQUEST
    if form.validate_on_submit():

        def m2_to_cm2(m2):
            return m2 * 10000

        def num_plants(field_cultivation_area, crop):
            area_in_cm2 = m2_to_cm2(field_cultivation_area) # cm2
            distance_rows_and_columns = sqrt(area_in_cm2) # cm. since we receive an area instead of a shape, we assumed is perfect square
            num_of_rows = (floor(distance_rows_and_columns / crop._space_x))/2 #
            num_of_cols = (floor(distance_rows_and_columns / crop._space_y))/2 # since space of plant and space for walk is the same DIVIDE by 2
            num_of_plants = num_of_rows * num_of_cols
            return num_of_plants

        # USER OBJS
        user_id = current_user.get_id()
        user = User.query.filter_by(id = user_id).first()
        farm = user.farms.filter_by(id = form.farm_choices.data).first()

        # VALIDATE FIELD AREA
        def validate_area():
            farm_area = farm.farm_area # in cm2
            fields_in_farm = farm.fields.all()
            sum_areas = 0

            for each_field in fields_in_farm:
                if each_field.id != field.id:
                    sum_areas += each_field.field_cultivation_area # in cm2
            new_area = m2_to_cm2(form.field_cultivation_area.data) # in cm2

            result = farm_area - sum_areas - new_area

            if result < 0:
                return False
            return True

        if not validate_area():
            flash('Your new crop area should not exceed the available land on your farm: {}'.format(farm.farm_name))
            return render_template('farm_settings/edit_crop.html', form=form, field_id = field.id)

        # FIELD OBJS TO DB
        field.field_cultivation_area = m2_to_cm2(form.field_cultivation_area.data) # in m2
        field.field_cultivation_start_date = form.field_cultivation_start_date.data
        field.field_cultivation_state = form.field_cultivation_state.data
        field.field_cultivation_type = form.field_cultivation_type.data

        # Calculated vars
        field.field_cultivation_finish_date = field.field_cultivation_start_date + timedelta(crop._dtg + crop._dtm) # datetime
        field.field_num_plants = num_plants(field_cultivation_area = form.field_cultivation_area.data, crop = crop) # number Integer
        field.field_projected_yield = crop._yield * field.field_num_plants # gr
        field.field_water_required_day = field.field_num_plants * crop._water

        # DB COMMANDS
        db.session.commit()

        #SUCESS AND REDIRECT TO DASHBOARD
        flash('You just edited field: {} in your farm: {}'.format(field.field_name, farm.farm_name))
        return redirect(url_for('settings.index'))
    return render_template('farm_settings/edit_crop.html', form=form, field_id = field_id)


##################
# USER DELETE CROP
##################
@farm_settings.route('/delete-crop/<field_id>', methods=['GET'])
@login_required
def delete_crop(field_id):

    try:
        field_to_del = Field.query.filter_by(id = field_id).first()
        farm = Farm.query.filter_by(id = field_to_del.farm_id).first()
        db.session.delete(field_to_del)
        db.session.commit()
        flash('You just deleted field: {} in your farm: {}'.format(field_to_del.field_name, farm.farm_name))
        return redirect(url_for('settings.index'))
    except Exception as e:
        flash('Error: ' + str(e))
        db.session.rollback()
    else:
        pass
    finally:
        pass


    flash('Error in TRY')
    return render_template('settings/index.html')
