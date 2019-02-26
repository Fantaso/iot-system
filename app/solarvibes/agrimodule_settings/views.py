from flask import Blueprint, render_template, redirect, url_for, flash, session
from solarvibes import db
from solarvibes.agrimodule_settings.forms import NewAgrimoduleForm, AgrimoduleAddSensorForm, PreEditAgrimoduleForm, EditAgrimoduleForm, PreEditAgripumpForm, EditAgripumpForm
from solarvibes.models import Crop, Farm, Field, Pump, Agrimodule, Agrisensor, Agripump
from solarvibes.models import AgrimoduleList, AgripumpList, AgrisensorList
from flask_login import current_user
from flask_security import login_required


agrimodule_settings = Blueprint(
    'agrimodule_settings',
    __name__,
    template_folder="templates"
)


###################
# USER NEW AGRIMODULE
###################
@agrimodule_settings.route('/new-agrimodule', methods=['GET', 'POST'])
@login_required
def new_agrimodule():
    # if agrimodule is register in solarvibes db
    def is_registered_in_solarvibes(identifier):
        agrimodule_reg = AgrimoduleList.query.filter_by(identifier = identifier).first()
        if not agrimodule_reg:
            return False
        return True
    # if a farmer has already registered this to him
    def is_registered_by_diff_user(identifier):
        agrimodule_reg = AgrimoduleList.query.filter_by(identifier = identifier).first()
        if agrimodule_reg:
            if agrimodule_reg.has_user_registered and current_user.id != agrimodule_reg.user_id:
                return True
            return False
        return False
    # if a farmer has already registered this agrimodule to his farm and is monitoring already a field for him
    def is_in_used_by_current_user(identifier):
        agrimodule_reg = AgrimoduleList.query.filter_by(identifier = identifier).first()
        agrimodule = Agrimodule.query.filter_by(identifier= identifier).first()
        if agrimodule_reg and agrimodule:
            if agrimodule_reg.has_user_registered and current_user.id == agrimodule.user_id and agrimodule.field_id:
                return True
            return False
        return False
    # if agrimodule is not monitoring a field is his farm but is already registered under his name and just need to link it to a field to monitor.
    def is_registered_by_current_user(identifier):
        agrimodule_reg = AgrimoduleList.query.filter_by(identifier = identifier).first()
        agrimodule = Agrimodule.query.filter_by(identifier= identifier).first()
        if agrimodule_reg and agrimodule:
            if agrimodule_reg.has_user_registered and current_user.id == agrimodule.user_id:
                return True
            return False
        return False

    # TODO: validate that can be installed in a field where there is already one

    def get_farm_name(id):
        return current_user.farms.filter_by(id = id).first().farm_name
    def get_farm_location(id):
        return current_user.farms.filter_by(id = id).first().farm_location
    def cm2_to_m2(cm2):
            return cm2 / 10000

    # Get list of all fields
    farms = current_user.farms.all()
    field_choices = []
    for farm in farms:
        for field in farm.fields.all():
            field_choices.append(field)

    # declare form
    form = NewAgrimoduleForm()
    # add dynamic choices
    form.field_choices.choices = [ (field.id, field.field_name + ' ' + str(cm2_to_m2(field.field_cultivation_area)) + ' m2 ' + get_farm_location(field.farm_id) + ' ' + get_farm_name(field.farm_id)) for field in field_choices ]
    form.field_choices.choices.insert(0, (0 ,'Choose:'))

    if form.validate_on_submit():
        if not is_registered_in_solarvibes(form.identifier.data):
            flash('agrimodule not registered in Solarvibes!', 'Contact Solarvibes support')
            return redirect(url_for('settings.index'))
        if is_registered_by_diff_user(form.identifier.data):
            flash('agrimodule is registered to another farmer!', 'Contact Solarvibes support')
            return redirect(url_for('settings.index'))
        if is_in_used_by_current_user(form.identifier.data):
            flash('agrimodule is already monitoring in your farms.', 'go to "farm settings -> agrimodule settings" and check which field is monitoring')
            return redirect(url_for('settings.index'))
        if is_registered_by_current_user(form.identifier.data):
            flash('agrimodule is already registered in your farm.', 'go to "farm settings -> agrimodule settings" and put it to monitor a field in your farm')
            return redirect(url_for('settings.index'))

        def val_choice(choice_id):
            if choice_id == 0:
                return None
            return choice_id

        # ADD AGRISYS OBJS
        name = form.name.data
        identifier = form.identifier.data
        field_choice = form.field_choices.data
        # print(name, identifier, lat, lon, field_choice)

        # OBJS TO DB
        agrimodule = Agrimodule(user = current_user,
                                name = name,
                                identifier = identifier,
                                lat = 0,
                                lon = 0,
                                batt_status = 0,
                                field_id = val_choice(field_choice))
        print(agrimodule.field_id)

        # update the registration form of agrimodule bundle
        agrimodule_reg = AgrimoduleList.query.filter_by(identifier = identifier).first()
        agrimodule_reg.has_user_registered = True
        agrimodule_reg.user_id = current_user.id

        # DB COMMANDS
        db.session.add(agrimodule)
        db.session.commit()

        # FLASH AND REDIRECT
        flash('You just added a new agrimodule: {}'.format(name))
        flash('Your agrimodule has been registered with identifier: "{}"'.format(identifier))
        return redirect(url_for('settings.index'))
    return render_template('agrimodule_settings/new_agrimodule.html', form=form)


##################
# USER EDIT AGRIMODULE
##################
@agrimodule_settings.route('/edit-agrimodule', methods=['GET', 'POST'])
@agrimodule_settings.route('/edit-agrimodule/<agrimodule_id>', methods=['GET', 'POST'])
@login_required
def edit_agrimodule(agrimodule_id = 0):
    # TODO: when disconnect and no field assigned before, None type error. sqlalchemy nonetype
    if int(agrimodule_id) <= 0:
        flash('This Agrimodule done not exist.')
        return redirect(url_for('main.index'))

    agrimodule_to_edit = current_user.agrimodules.filter_by(id = agrimodule_id).first()
    myAgrimodule = PreEditAgrimoduleForm(name = agrimodule_to_edit.name, field_choices = agrimodule_to_edit.field_id)

    form = EditAgrimoduleForm(obj = myAgrimodule)

    #TODO: validate that only fields which are not being currently monitored can be pass to the choices
    farms = current_user.farms.all()
    field_choices = []
    for farm in farms:
        for field in farm.fields.all():
            field_choices.append(field)

    def get_farm_name(id):
        return current_user.farms.filter_by(id = id).first().farm_name
    def get_farm_location(id):
        return current_user.farms.filter_by(id = id).first().farm_location
    def cm2_to_m2(cm2):
            return cm2 / 10000
    form.field_choices.choices = [ (field.id, field.field_name + ' ' + str(cm2_to_m2(field.field_cultivation_area)) + ' m2 ' + get_farm_location(field.farm_id) + ' ' + get_farm_name(field.farm_id)) for field in field_choices ]
    form.field_choices.choices.insert(0, (0 ,'Choose:'))
    form.field_choices.choices.append((1000 ,'Disconnect!'))
    # form.field_choices.choices = [ (field.id, field.field_name + ' ' + str(cm2_to_m2(field.field_cultivation_area)) + ' m2 ' + get_farm_location(field.farm_id) + ' ' + get_farm_name(field.farm_id)) for field in field_choices ]
    if form.validate_on_submit():   # IF request.methiod == 'POST'
        # if agrimodule is already in that field
        def has_agrimodule(field_id):
            if Agrimodule.query.filter_by(field_id = field_id).count() > 0:
                return True
            return False
        def same_agrimodule(form_field_id, agrimodule_to_edit_pump_id):
            if agrimodule_to_edit_pump_id == form_field_id:
                return True
            return False

        if same_agrimodule(form.field_choices.data, agrimodule_to_edit.field_id):
            field = Field.query.filter_by(id = form.field_choices.data).first()
            flash('Nothing changed. You are already monitoring the field: {}!'.format(field.field_name))
            return redirect(url_for('settings.index'))
        if has_agrimodule(form.field_choices.data):
            agrimodule = current_user.agrimodules.filter_by(field_id = form.field_choices.data).first()
            flash('That field is being monitored already by agrimodule: {}'.format(agrimodule.name))
            return redirect(url_for('agrimodule_settings.edit_agrimodule', form=form, agrimodule_id = agrimodule_id))

        # REST OF FORM HANDLING
        if form.field_choices.data == 0:
            flash('Nothing changed!'.format())
        elif form.field_choices.data == 1000:
            field = Field.query.filter_by(id = agrimodule_to_edit.field_id).first()
            flash('You just disconnected your agrimodule {} from field: {}'.format(agrimodule_to_edit.name, field.field_name))
            agrimodule_to_edit.field_id = None
        else:
            field = Field.query.filter_by(id = form.field_choices.data).first()
            flash('You just change your agrimodule {} to monitor: {}'.format(agrimodule_to_edit.name, field.field_name ))
            agrimodule_to_edit.field_id = form.field_choices.data

        agrimodule_to_edit.name = form.name.data
        db.session.commit()

        return redirect(url_for('settings.index'))
    return render_template('agrimodule_settings/edit_agrimodule.html', form=form, agrimodule_to_edit=agrimodule_to_edit)


##################
# USER ADD SENSOR
##################
@agrimodule_settings.route('/add-sensor', methods=['GET', 'POST'])
@agrimodule_settings.route('/add-sensor/<agrimodule_id>', methods=['GET', 'POST'])
@login_required
def add_sensor(agrimodule_id = 0):
    ##############      AGRIPUMP     ######################
    # if agrimodule is register in solarvibes db
    def agripump_is_registered_in_solarvibes(identifier):
        agripump_reg = AgripumpList.query.filter_by(identifier = identifier).first()
        if not agripump_reg:
            return False
        return True
    # if a farmer has already registered this to him
    def agripump_is_registered_by_diff_user(identifier):
        agripump_reg = AgripumpList.query.filter_by(identifier = identifier).first()
        if agripump_reg:
            if agripump_reg.has_user_registered and current_user.id != agripump_reg.user_id:
                return True
            return False
        return False
    # TODO: this is just if user registered it. but if user deleted and wants to added again - check if the users agripump current list is there.
    # if a farmer has already registered this agrimodule to his farm and is monitoring already a field for him
    def agripump_is_in_used_by_current_user(identifier):
        agripump_reg = AgripumpList.query.filter_by(identifier = identifier).first()
        agripump = Agripump.query.filter_by(identifier= identifier).first()
        agrimodule = Agrimodule.query.filter_by(id = agripump.agrimodule_id).first()
        if agripump_reg and agripump and agrimodule:
            if agripump_reg.has_user_registered and current_user.id == agripump_reg.user_id:
                return True
            return False
        return False
    def agripump_is_registered_by_current_user(identifier):
        agripump_reg = AgripumpList.query.filter_by(identifier = identifier).first()
        if agrimpump_reg:
            if agripump_reg.has_user_registered and current_user.id == agripump_reg.user_id:
                return True
            return False
    ##############      AGRIPUMP     ######################

    ##############      AGRISENSOR     ######################
    # if agrimodule is register in solarvibes db
    def agrisensor_is_registered_in_solarvibes(identifier):
        agrisensor_reg = AgrisensorList.query.filter_by(identifier = identifier).first()
        if not agrisensor_reg:
            return False
        return True
    # if a farmer has already registered this to him
    def agrisensor_is_registered_by_diff_user(identifier):
        agrisensor_reg = AgrisensorList.query.filter_by(identifier = identifier).first()
        if agrisensor_reg:
            if agrisensor_reg.has_user_registered and current_user.id != agrisensor_reg.user_id:
                return True
            return False
        return False
    def agrisensor_is_in_used_by_current_user(identifier):
        agrisensor_reg = AgripumpList.query.filter_by(identifier = identifier).first()
        agrisensor = Agrisensor.query.filter_by(identifier= identifier).first()
        agrimodule = Agrimodule.query.filter_by(id = agrisensor.agrimodule_id).first()
        if agrisensor_reg and agrisensor and agrimodule:
            if agrisensor_reg.has_user_registered and current_user.id == agrisensor_reg.user_id:
                return True
            return False
        return False
    def agrisensor_is_registered_by_current_user(identifier):
        agrisensor_reg = AgrisensorList.query.filter_by(identifier = identifier).first()
        if agrisensor_reg.has_user_registered and current_user.id == agrisensor_reg.user_id:
            return True
        return False
    ##############      AGRISENSOR     ######################

    form = AgrimoduleAddSensorForm()
    if int(agrimodule_id) <= 0:
        agrimodule_choices = current_user.agrimodules.all()
        form.agrimodule_choices.choices = [ (agrimodule.id, agrimodule.name) for agrimodule in agrimodule_choices ] # AGRIMODULE
        form.agrimodule_choices.choices.insert(0, ('0' ,'Choose:'))
    else:
        agrimodule = current_user.agrimodules.filter_by(id = agrimodule_id).first()
        form.agrimodule_choices.choices = [ (agrimodule.id, agrimodule.name) ] # AGRIMODULE

    ##############          POST REQUEST             #########################
    if form.validate_on_submit():   # IF request.methiod == 'POST'
        agrimodule_id = form.agrimodule_choices.data
        sensor_type = form.sensor_choices.data
        identifier = form.identifier.data
        ###################          AGRIPUMPPP         ###############
        if sensor_type == 'Agripump':
            if not agripump_is_registered_in_solarvibes(form.identifier.data):
                flash('agripump not registered in Solarvibes!', 'Contact Solarvibes support')
                return redirect(url_for('settings.index'))
            if agripump_is_registered_by_diff_user(form.identifier.data):
                flash('agripump is registered to another farmer!', 'Contact Solarvibes support')
                return redirect(url_for('settings.index'))
            if agripump_is_in_used_by_current_user(form.identifier.data):
                flash('agripump is already connected to an agrimodule in your farm.', 'go to "farm settings -> agrimodule settings" and check whicha grimodule is connected to')
                return redirect(url_for('settings.index'))
            if agripump_is_registered_by_current_user(form.identifier.data):
                flash('agripump is already registered in your farm.', 'go to "farm settings -> agrimodule settings" and check which agrimodule is connected to your agripump')
                return redirect(url_for('settings.index'))

            agripump = Agripump(agrimodule_id = agrimodule_id, identifier = identifier, status = False, lat = 0, lon = 0)
            db.session.add(agripump)
            # update the registration form of agrimodule bundle
            agripump_reg = AgripumpList.query.filter_by(identifier = identifier).first()
            agripump_reg.has_user_registered = True
            agripump_reg.user_id = current_user.id

        #################       AGRISENSOR          ######################################
        if sensor_type == 'Agrisensor':
            if not agrisensor_is_registered_in_solarvibes(form.identifier.data):
                flash('agrisensor not registered in Solarvibes!', 'Contact Solarvibes support')
                return redirect(url_for('settings.index'))
            if agrisensor_is_registered_by_diff_user(form.identifier.data):
                flash('agrisensor is registered to another farmer!', 'Contact Solarvibes support')
                return redirect(url_for('settings.index'))
            if agrisensor_is_in_used_by_current_user(form.identifier.data):
                flash('agrisensor is already connected to an agrimodule in your farm.', 'go to "farm settings -> agrimodule settings" and check which agrimodule is connected to')
                return redirect(url_for('settings.index'))
            if agrisensor_is_registered_by_current_user(form.identifier.data):
                flash('agrisensor is already registered in your farm', 'go to "farm settings -> agrimodule settings" and check which agrimodule is connected to your agrisensor')
                return redirect(url_for('settings.index'))

            agrisensor = Agrisensor(agrimodule_id = agrimodule_id, identifier = identifier, batt_status = 0, lat = 0, lon = 0)
            db.session.add(agrisensor)

            # update the registration form of agrimodule bundle
            agrisensor_reg = AgrisensorList.query.filter_by(identifier = identifier).first()
            agrisensor_reg.has_user_registered = True
            agrisensor_reg.user_id = current_user.id

        # DB COMMANDS
        db.session.commit()
        flash('You just added an {}: {} in your system: {}'.format(sensor_type, identifier, Agrimodule.query.filter_by(id = agrimodule_id).first().name))
        return redirect(url_for('settings.index'))
    return render_template('agrimodule_settings/add_sensor.html', form=form)


##################
# USER EDIT AGRIPUMP
##################
@agrimodule_settings.route('/edit-agripump/', methods=['GET', 'POST'])
@agrimodule_settings.route('/edit-agripump/<agripump_id>', methods=['GET', 'POST'])
@login_required
def edit_agripump(agripump_id = 0):

    # TODO: when disconnect and no pump assigned before, None type error. sqlalchemy nonetype
    # validate thats is an valid id # add later the query if id actually exist
    if int(agripump_id) <= 0:
        flash('This Agripump done not exist.')
        return redirect(url_for('settings.index'))

    # pass to template
    agripump_to_edit = Agripump.query.filter_by(id = agripump_id).first()

    myAgripump = PreEditAgripumpForm(pump_choices = agripump_to_edit.pump_id)
    pump_choices = current_user.pumps.all()

    # Prepopulate form
    form = EditAgripumpForm(obj = myAgripump)
    form.pump_choices.choices = [ (pump.id, pump.pump_name) for pump in pump_choices ] # PUMP
    form.pump_choices.choices.insert(0, (0 ,'Choose:'))
    form.pump_choices.choices.append((1000 ,'Disconnect!'))



    if form.validate_on_submit():   # IF request.methiod == 'POST'
        # FIELD OBJS  TO DB
        try:
            # if agrimodule is already in that field
            def has_agripump(pump_id):
                if Agripump.query.filter_by(pump_id = pump_id).count() > 0:
                    return True
                else:
                    return False
            def same_agripump(form_pump_id, agripump_to_edit_pump_id):
                if agripump_to_edit_pump_id == form_pump_id:
                    return True
                else:
                    return False

            if same_agripump(form.pump_choices.data, agripump_to_edit.pump_id):
                pump = Pump.query.filter_by(id = form.pump_choices.data).first()
                flash('Nothing changed. You are already controlling the pump: {}!'.format(pump.pump_name))
                return redirect(url_for('settings.index'))

            if has_agripump(form.pump_choices.data):
                agripump = Agripump.query.filter_by(pump_id = form.pump_choices.data).first()
                pump = Pump.query.filter_by(id = form.pump_choices.data).first()
                flash('That pump {} is controlled already by agripump: {}'.format(pump.pump_name, agripump.identifier))
                return redirect(url_for('agrimodule_settings.edit_agripump', form=form, agripump_id = agripump_id))

            # REST OF FORM HANDLING
            if form.pump_choices.data == 0:
                flash('Nothing changed!'.format())
            elif form.pump_choices.data == 1000:
                pump = current_user.pumps.filter_by(id = agripump_to_edit.pump_id).first()
                flash('You just disconnected your agripump from pump: {}'.format(pump.pump_name))
                agripump_to_edit.pump_id = None
            else:
                pump = current_user.pumps.filter_by(id = form.pump_choices.data).first()
                agripump_to_edit.pump_id = form.pump_choices.data
                flash('You just change your agripumps pump to work on pump: {}'.format(pump.pump_name))

            # DB COMMANDS
            db.session.commit()

            return redirect(url_for('settings.index'))
        except Exception as e:
            flash('Error: ' + str(e))
            db.session.rollback()
            return redirect(url_for('settings.index'))
    return render_template('agrimodule_settings/edit_agripump.html', form=form, agripump_to_edit = agripump_to_edit)


##################
# USER DELETE AGRIMODULE
##################
@agrimodule_settings.route('/delete-agrimodule', methods=['GET'])
@agrimodule_settings.route('/delete-agrimodule/<agrimodule_id>', methods=['GET'])
@login_required
# //TODO: erase from agrimodulelist the .has_user_registered when deleting an agrimodule from the system
def delete_agrimodule(agrimodule_id = 0):
    if int(agrimodule_id) <= 0:
        flash('This Agrimodule done not exist.')
        return redirect(url_for('settings.index'))

    try:
        agrimodule = current_user.agrimodules.filter_by(id = agrimodule_id).first()

        agripumps = agrimodule.agripumps.all()
        agripumps_qty = agrimodule.agripumps.count()

        agrisensors = agrimodule.agrisensors.all()
        agrisensors_qty = agrimodule.agrisensors.count()

        for agripump in agripumps:
            db.session.delete(agripump)
        for agrisensor in agrisensors:
                db.session.delete(agrisensor)
        db.session.delete(agrimodule)
        db.session.commit()
        flash('You just deleted agrimodule: {}, with {} agripumps and {} agrisensors'.format(agrimodule.name, agripumps_qty, agrisensors_qty))
        return redirect(url_for('settings.index'))
    except Exception as e:
        flash('Error: ' + str(e))
        db.session.rollback()
        return render_template('settings/index.html')

    flash('You just deleted agrimodule: {}'.format('agrimodule name'))
    return render_template('settings/index.html')


##################
# USER DELETE AGRIPUMP
##################
@agrimodule_settings.route('/delete-agripump', methods=['GET'])
@agrimodule_settings.route('/delete-agripump/<agripump_id>', methods=['GET'])
@login_required
def delete_agripump(agripump_id = 0):
    if int(agripump_id) <= 0:
        flash('This Agripump done not exist.')
        return redirect(url_for('settings.index'))

    try:
        agripump_to_del = Agripump.query.filter_by(id = agripump_id).first()
        db.session.delete(agripump_to_del)
        db.session.commit()
        flash('You just deleted agripump: {}'.format(agripump_to_del.identifier))
        return redirect(url_for('settings.index'))
    except Exception as e:
        flash('Error: ' + str(e))
        db.session.rollback()
        return render_template('settings/index.html')
    else:
        pass
    finally:
        pass


    flash('Error in Delete_Agripump')
    return render_template('settings/index.html')


##################
# USER DELETE AGRISENSOR
##################
@agrimodule_settings.route('/delete-agrisensor', methods=['GET'])
@agrimodule_settings.route('/delete-agrisensor/<agrisensor_id>', methods=['GET'])
@login_required
def delete_agrisensor(agrisensor_id = 0):
    try:
        agrisensor_to_del = Agrisensor.query.filter_by(id = agrisensor_id).first()
        db.session.delete(agrisensor_to_del)
        db.session.commit()
        flash('You just deleted agrisensor: {}'.format(agrisensor_to_del.identifier))
        return redirect(url_for('settings.index'))
    except Exception as e:
        flash('Error: ' + str(e))
        db.session.rollback()
        return render_template('settings/index.html')
    else:
        pass
    finally:
        pass

    flash('Error in Delete_Agrisensor')
    return render_template('settings/index.html')
