from flask import Blueprint, render_template, redirect, url_for, flash, session
from solarvibes import db
from solarvibes.welcome.forms import PreAddFarmForm, AddFarmForm, PreAddSoilTestForm, AddSoilTestForm, PreAddWaterTestForm, AddWaterTestForm, AddCropForm, PreAddCropForm, AddAgrisysForm, PreAddAgrisysForm, InstallAgrisysForm, PreInstallAgrisysForm, AddPumpForm, PreAddPumpForm
from solarvibes.models import User, Crop, Farm, Field, Pump, Agrimodule, Agrisensor, Agripump, SoilTest, WaterTest
from solarvibes.models import AgrimoduleList, AgrisensorList, AgripumpList
from solarvibes.models import WelcomeLog
from flask_login import current_user
from flask_security import login_required
from math import sqrt, floor
from datetime import datetime, timedelta

welcome = Blueprint(
    'welcome',
    __name__,
    template_folder="templates"
)

#############################
#############################
# WELCOME VIEWS
#############################
#############################

###################
# WELCOME
###################
@welcome.route('/', methods=['GET'])
@login_required
def index():
    if 'welcome' not in session:
        session['welcome'] = dict()
        session.modified = True

    # if user hasnot yet a welcome_log, then created
    if not current_user.welcome:
        welcome_log = WelcomeLog(   user = current_user,
                                    add_agrisys = False,
                                    install_agrisys = False,
                                    add_pump = False,
                                    add_farm = False,
                                    add_soil_test = False,
                                    add_water_test = False,
                                    add_field = False)
        db.session.add(welcome_log)
        db.session.commit()

    # if user have not set up any agrimodule -> we send him to set agrimodule first
    if not current_user.welcome.add_agrisys or not current_user.welcome.install_agrisys or not current_user.welcome.add_pump:
        flash('welcome for the first time, ' + current_user.name + '!')
        set_sys_flag = True
        return render_template('welcome/welcome.html', user=current_user, set_sys_flag=set_sys_flag)

    # if user have not set up any farm yet -> we send him to set his farm only
    if not current_user.welcome.add_farm or current_user.welcome.add_field:
        flash('Now set your farm, ' + current_user.name + '!')
        set_sys_flag = False
        return render_template('welcome/welcome.html', user=current_user, set_sys_flag=set_sys_flag)

    # if neither the case send him to main. he must have set up a system and a farm
    else:
        flash('you already have install agrimodule and add it to your farm, ' + current_user.name + '!')
        return redirect(url_for('main.index'))


###################
# SET CONNECT ASS
###################
@welcome.route('/add-agrisys', methods=['GET', 'POST'])
@login_required
def add_agrisys():

    if 'welcome' not in session:
        session['welcome'] = dict()
        session.modified = True

    form = AddAgrisysForm()
    # if user has complete farm, but didnot finish field. pass the current
    if current_user.welcome.add_agrisys:
        agrimodule = current_user.agrimodules.first()
        myAgrimodule = PreAddAgrisysForm(agrimodule_name = agrimodule.name, agrimodule_identifier = agrimodule.identifier)
        form = AddAgrisysForm(obj=myAgrimodule)               # CREATE WTForm FORM

    if form.validate_on_submit():
        # USER OBJS
        user = current_user

        # ADD AGRISYS OBJS
        agrimodule_name = form.agrimodule_name.data
        agrimodule_identifier = form.agrimodule_identifier.data

        # if agrimodule is register in solarvibes db
        def is_registered_in_solarvibes(identifier):
            agrimodule_reg = AgrimoduleList.query.filter_by(identifier = identifier).first()
            if not agrimodule_reg:
                return False
            return True

        # if a farmer has already registered this to him
        def is_registered_by_diff_user(identifier):
            agrimodule_reg = AgrimoduleList.query.filter_by(identifier = identifier).first()
            if agrimodule_reg.has_user_registered and current_user.id != agrimodule_reg.user_id:
                return True
            return False

        # if end with tripple zero ("0") belongs to the bundle
        def is_agrimodule_bundle(identifier):
            if identifier[-3:] == '000':
                return True
            return False

        def get_bundle_identifiers(identifier):
            agrimodule_identifier = identifier
            # //TODO: must recognize all numbers instead of the las four digits. unless a uuid is created with a standarz characters qty.
            agrisensor_identifier = 'agrisensor' + identifier[-5:]
            agripump_identifier = 'agripump' + identifier[-5:]
            return agrimodule_identifier, agrisensor_identifier, agripump_identifier

        if not is_registered_in_solarvibes(agrimodule_identifier):
            flash('agrimodule not registered in Solarvibes! Contact Solarvibes support')
            return redirect(url_for('welcome.add_agrisys', form = form))

        if is_registered_by_diff_user(agrimodule_identifier):
            flash('agrimodule is registered to another farmer! Contact Solarvibes support')
            return redirect(url_for('welcome.add_agrisys', form = form))

        try:
            if is_agrimodule_bundle(agrimodule_identifier):

                agrimodule_identifier, agrisensor_identifier, agripump_identifier = get_bundle_identifiers(agrimodule_identifier)

                if current_user.welcome.add_agrisys:
                    # OBJS TO DB
                    agrimodule = current_user.agrimodules.first()
                    agrimodule.name = agrimodule_name
                    agrimodule.identifier = agrimodule_identifier
                    agrisensor = agrimodule.agrisensors.first()
                    agrisensor.identifier = agrisensor_identifier
                    agripump = agrimodule.agripumps.first()
                    agripump.identifier = agripump_identifier

                    # FLASH
                    flash('Your agrimodule bundle has been re-registered with identifier: "{}"'.format(agrimodule_identifier))
                else:
                    # OBJS TO DB
                    agrimodule = Agrimodule(name = agrimodule_name, identifier = agrimodule_identifier, user = user, batt_status = 0, lat = 0, lon = 0)
                    agrisensor = Agrisensor(identifier = agrisensor_identifier, agrimodule = agrimodule, batt_status = 0, lat = 0, lon = 0)
                    agripump = Agripump(identifier = agripump_identifier, agrimodule = agrimodule, status = False, lat = 0, lon = 0)
                    # DB COMMANDS
                    db.session.add_all([agrimodule, agrisensor, agripump])
                    # FLASH
                    flash('Your agrimodule bundle has been registered with identifier: "{}"'.format(agrimodule_identifier))

                # update the registration form of agrimodule bundle
                agrimodule_reg = AgrimoduleList.query.filter_by(identifier = agrimodule_identifier).first()
                agrisensor_reg = AgrisensorList.query.filter_by(identifier = agrisensor_identifier).first()
                agripump_reg = AgripumpList.query.filter_by(identifier = agripump_identifier).first()
                agrimodule_reg.has_user_registered = True
                agrimodule_reg.user_id = user.id
                agrisensor_reg.has_user_registered = True
                agrisensor_reg.user_id = user.id
                agripump_reg.has_user_registered = True
                agripump_reg.user_id = user.id
            else:
                if current_user.welcome.add_agrisys:
                    # OBJS TO DB
                    agrimodule = current_user.agrimodules.first()
                    agrimodule.name = agrimodule_name
                    agrimodule.identifier = agrimodule_identifier
                    # FLASH
                    flash('Your agrimodule has been re-registered with identifier: "{}"'.format(agrimodule_identifier))
                else:
                    # OBJS TO DB
                    agrimodule = Agrimodule(name = agrimodule_name, identifier = agrimodule_identifier, user = user)
                    # DB COMMANDS
                    db.session.add(agrimodule)
                    # FLASH
                    flash('Your agrimodule has been registered with identifier: "{}"'.format(agrimodule_identifier))

                # update the registration form of agrimodule bundle
                agrimodule_reg = AgrimoduleList.query.filter_by(identifier = agrimodule_identifier).first()
                agrimodule_reg.has_user_registered = True
                agrimodule_reg.user_id = user.id

            # set welcome flag to True
            user.welcome.add_agrisys = True
            # DB COMMANDS
            db.session.commit()
            # ADD SESSION OBJS
            session['welcome'].update({'agrimodule_identifier':agrimodule_identifier, 'agrimodule_id':agrimodule.id})
            session.modified = True

            # REDIRECT
            return redirect(url_for('welcome.install_agrisys'))
        except Exception as e:
            db.session.rollback()
            flash('Error: ' + str(e))
            flash('an error has occour. Try again later!'.format(agrimodule_identifier))
            return redirect(url_for('welcome.add_agrisys', form = form))
    return render_template('welcome/add_agrisys.html', form=form)



###################
# SET INSTALL ASS
###################
@welcome.route('/install-agrisys', methods=['GET', 'POST'])
@login_required
def install_agrisys():

    # def is_agrimodule_bundle(identifier):
    #     if identifier[-3:] == '000':
    #         return True
    #     return False
    #
    # def get_bundle_identifiers(identifier):
    #     agrimodule_identifier = identifier
    #     agrisensor_identifier = 'agrisensor' + identifier[-4:]
    #     agripump_identifier = 'agripump' + identifier[-4:]
    #     return agrimodule_identifier, agrisensor_identifier, agripump_identifier
    #
    # form = InstallAgrisysForm()
    # if form.validate_on_submit():
    #     # USER OBJS
    #     user = current_user
    #
    #     # INSTALL AGRISYS OBJS
    #     agm_lat = form.agm_lat.data
    #     agm_lon = form.agm_lon.data
    #     ags_lat = form.ags_lat.data
    #     ags_lon = form.ags_lon.data
    #     agp_lat = form.agp_lat.data
    #     agp_lon = form.agp_lon.data
    #     print (form.agm_lat)
    #     print (form.agm_lon)
    #     print (form.ags_lat)
    #     print (form.ags_lon)
    #     print (form.agp_lat)
    #     print (form.agp_lon)
    #
    #     # OBJS TO DB
    #     agrimodule_id = session['set_sys']['agrimodule_id']
    #     agrisensor  = Agrisensor(agrimodule_id = agrimodule_id, lat = ags_lat, lon = ags_lon)
    #     agripump    =   Agripump(agrimodule_id = agrimodule_id, lat = agp_lat, lon = agp_lon)
    #     agrimodule = Agrimodule.query.filter_by(id = agrimodule_id).first()
    #     agrimodule.lat = agm_lat
    #     agrimodule.lon = agm_lon
    #     print(agrimodule_id)
    #     print(agrisensor)
    #     print(agripump)
    #
    #     # DB COMMANDS
    #     db.session.add(agrisensor)
    #     db.session.add(agripump)
    #     db.session.commit()
    #
    #     # ADD SESSION OBJS
    #     session['set_sys'].update({'agrimodule_id':agrimodule.id, 'agrisensor_id':agrisensor.id, 'agripump_id':agripump.id, 'agm_lat':agm_lat, 'agm_lon':agm_lon, 'ags_lat':ags_lat, 'ags_lon':ags_lon, 'agp_lat':agp_lat, 'agp_lon':agp_lon})
    #     session.modified = True
    #     print (session['set_sys'])
    #
    #
    #
    #     # FLASH AND REDIRECT
    #     flash('''Your Agrimodule location is: LAT: {} LON: {}
    #             Your Agrisensor location is: LAT: {} LON: {}
    #             Your Agripump location is: LAT: {} LON: {}'''.format(agm_lat, agm_lon, ags_lat, ags_lon, agp_lat, agp_lon))
        # return redirect(url_for('welcome.add_pump'))
    current_user.welcome.install_agrisys = True
    db.session.commit()
    return render_template('welcome/install_agrisys.html')

###################
# SET ADD PUMP
###################
@welcome.route('/add-pump', methods=['GET', 'POST'])
@login_required
def add_pump():
    if 'welcome' not in session:
        session['welcome'] = dict()
        session.modified = True
    # from form to db
    def lps_to_mlpm(lps):
        return lps * (1000 * 60)
    def m_to_cm(m):
        return m * 100
    def kw_to_w(kw):
        return kw * 1000
    # from db to form
    def mlpm_to_lps(mlpm):
        return mlpm / (1000 * 60)
    def cm_to_m(cm):
        return cm / 100
    def w_to_kw(w):
        return w / 1000

    form = AddPumpForm()
    # if user has complete farm, but didnot finish field. pass the current
    if current_user.welcome.add_pump:
        pump = current_user.pumps.first()
        myPump = PreAddPumpForm(pump_name = pump.pump_name, pump_brand = pump.pump_brand, pump_flow_rate = mlpm_to_lps(pump.pump_flow_rate), pump_head = cm_to_m(pump.pump_head), pump_watts = w_to_kw(pump.pump_watts))
        form = AddPumpForm(obj=myPump)               # CREATE WTForm FORM

    if form.validate_on_submit():
        # USER OBJS
        user = current_user
        agrimodule = user.agrimodules.first()
        agripump = agrimodule.agripumps.first()

        if current_user.welcome.add_pump:
            pump.pump_name = form.pump_name.data
            pump.pump_brand = form.pump_brand.data
            pump.pump_flow_rate = lps_to_mlpm(form.pump_flow_rate.data)
            pump.pump_head = m_to_cm(form.pump_head.data)
            pump.pump_watts = kw_to_w(form.pump_watts.data)
            flash('Your pump has been re-registered: "{}"'.format(pump.pump_name))
        else:
            # ADD PUMP OBJS
            pump_name = form.pump_name.data
            pump_brand = form.pump_brand.data
            pump_flow_rate = lps_to_mlpm(form.pump_flow_rate.data)
            pump_head = m_to_cm(form.pump_head.data)
            pump_watts = kw_to_w(form.pump_watts.data)
            # OBJS TO DB
            pump = Pump(user = user, pump_name = pump_name, pump_brand = pump_brand, pump_flow_rate = pump_flow_rate, pump_head = pump_head, pump_watts = pump_watts)
            db.session.add(pump)
            flash('Your pump has been registered: "{}"'.format(pump.pump_name))

        # DB COMMANDS
        db.session.commit()

        # ADD PUMP TO AGRIPUMP
        if agripump:
            agripump.pump_id = pump.id
        current_user.welcome.add_pump = True
        db.session.commit()


        # OBJS SAVE ON SESSION
        session['welcome'].update({'pump_id':pump.id, 'pump_brand':form.pump_brand.data, 'pump_flow_rate':form.pump_flow_rate.data, 'pump_head':form.pump_head.data, 'pump_watts':form.pump_watts.data})
        session.modified = True


        # FLASH AND REDIRECT
        flash('''Your Pump brand: {}
                Flow rate: {} lps
                Head pressure: {} m
                Wattage: {} kW'''.format(form.pump_brand.data, form.pump_flow_rate.data, form.pump_head.data, form.pump_watts.data))
        return redirect(url_for('welcome.index'))

    return render_template('welcome/add_pump.html', form=form)

###################
# SET ADD SOIL TEST
###################
@welcome.route('/add-soil-test', methods=['GET', 'POST'])
@login_required
def add_soil_test():
    if 'welcome' not in session:
        session['welcome'] = dict()
        session.modified = True

    form = AddSoilTestForm()
    # if user has complete farm, but didnot finish field. pass the current
    if current_user.welcome.add_soil_test:
        soil_test = current_user.farms.first().soil_tests.first()
        mySoilTest = PreAddSoilTestForm(soil_ph = soil_test.soil_ph, soil_ec = soil_test.soil_ec, soil_organic_carbon = soil_test.soil_organic_carbon, soil_nitrogen=soil_test.soil_nitrogen, soil_p205=soil_test.soil_p205, soil_k20=soil_test.soil_k20)
        form = AddSoilTestForm(obj=mySoilTest)

    if form.validate_on_submit():
        # USER OBJS
        farm = current_user.farms.first()

        if current_user.welcome.add_soil_test:
            soil_test.soil_ph = form.soil_ph.data
            soil_test.soil_ec = form.soil_ec.data
            soil_test.soil_organic_carbon = form.soil_organic_carbon.data
            soil_test.soil_nitrogen = form.soil_nitrogen.data
            soil_test.soil_p205 = form.soil_p205.data
            soil_test.soil_k20 = form.soil_k20.data
            flash('Your soil test has been re-registered: "Soil Test ID {}"'.format(soil_test.id))
        else:
            # ADD SOIL TEST OBJS
            soil_ph = form.soil_ph.data
            soil_ec = form.soil_ec.data
            soil_organic_carbon = form.soil_organic_carbon.data
            soil_nitrogen = form.soil_nitrogen.data
            soil_p205 = form.soil_p205.data
            soil_k20 = form.soil_k20.data
            # OBJS TO DB
            soil_test = SoilTest(farm_id = farm.id, soil_ph = soil_ph, soil_ec = soil_ec, soil_organic_carbon = soil_organic_carbon, soil_nitrogen=soil_nitrogen, soil_p205=soil_p205, soil_k20=soil_k20)
            db.session.add(soil_test)
            flash('Your soil test has been registered: "Soil Test ID {}"'.format(soil_test.id))

        # DB COMMANDS
        db.session.commit()

        # SAVE INPUT STATUS
        current_user.welcome.add_soil_test = True
        db.session.commit()

        # OBJS SAVE ON SESSION
        session['welcome'].update({'soil_test_id':soil_test.id, 'soil_ph':form.soil_ph.data, 'soil_ec':form.soil_ec.data, 'soil_organic_carbon':form.soil_organic_carbon.data, 'soil_nitrogen':form.soil_nitrogen.data, 'soil_p205':form.soil_p205.data, 'soil_k20':form.soil_k20.data})
        session.modified = True

        # FLASH AND REDIRECT
        return redirect(url_for('welcome.add_water_test'))

    return render_template('welcome/add_soil_test.html', form=form)


###################
# SET ADD WATER TEST
###################
@welcome.route('/add-water-test', methods=['GET', 'POST'])
@login_required
def add_water_test():
    if 'welcome' not in session:
        session['welcome'] = dict()
        session.modified = True

    form = AddWaterTestForm()
    # if user has complete farm, but didnot finish field. pass the current
    if current_user.welcome.add_water_test:
        water_test = current_user.farms.first().water_tests.first()
        myWaterTest = PreAddWaterTestForm(water_ph = water_test.water_ph, water_ec = water_test.water_ec, water_bicarbonates = water_test.water_bicarbonates, water_carbonates = water_test.water_carbonates, water_potasium= water_test.water_potasium, water_sulphate=water_test.water_sulphate)
        form = AddWaterTestForm(obj=myWaterTest)

    if form.validate_on_submit():
        # USER OBJS
        farm = current_user.farms.first()

        if current_user.welcome.add_water_test:
            water_test.water_ph = form.water_ph.data
            water_test.water_ec = form.water_ec.data
            water_test.water_bicarbonates = form.water_bicarbonates.data
            water_test.water_carbonates = form.water_carbonates.data
            water_test.water_potasium = form.water_potasium.data
            water_test.water_sulphate = form.water_sulphate.data
            flash('Your water test has been re-registered: "Water Test ID {}"'.format(water_test.id))
        else:
            # ADD WATER TEST OBJS
            water_ph = form.water_ph.data
            water_ec = form.water_ec.data
            water_bicarbonates = form.water_bicarbonates.data
            water_carbonates = form.water_carbonates.data
            water_potasium = form.water_potasium.data
            water_sulphate = form.water_sulphate.data
            # OBJS TO DB
            water_test = WaterTest(farm_id = farm.id, water_ph = water_ph, water_ec = water_ec, water_bicarbonates = water_bicarbonates, water_carbonates=water_carbonates, water_potasium=water_potasium, water_sulphate=water_sulphate)
            db.session.add(water_test)
            flash('Your water test has been registered: "Water Test ID {}"'.format(water_test.id))

        # DB COMMANDS
        db.session.commit()

        # SAVE INPUT STATUS
        current_user.welcome.add_water_test = True
        db.session.commit()

        # OBJS SAVE ON SESSION
        session['welcome'].update({'water_test_id':water_test.id, 'water_ph':form.water_ph.data, 'water_ec':form.water_ec.data, 'water_bicarbonates':form.water_bicarbonates.data, 'water_carbonates':form.water_carbonates.data, 'water_potasium':form.water_potasium.data, 'water_sulphate':form.water_sulphate.data})
        session.modified = True

        # FLASH AND REDIRECT
        return redirect(url_for('welcome.add_crop'))

    return render_template('welcome/add_water_test.html', form=form)

###################
# SET FARM
###################

@welcome.route('/add-farm', methods=['GET', 'POST'])
@login_required
def add_farm():

    def cm2_to_m2(cm2):
        return cm2 / 10000
    def m2_to_cm2(m2):
        return m2 * 10000

    if 'welcome' not in session:
        session['welcome'] = dict()
        session.modified = True

    form = AddFarmForm()

    # if user has complete farm, but did not finish field. pass the current
    if current_user.welcome.add_farm:

        farm = current_user.farms.first()

        myFarm = PreAddFarmForm(farm_name = farm.farm_name,
                            farm_location = farm.farm_location,
                            # farm_coordinates = farm.farm_coordinates,
                            farm_area = cm2_to_m2(farm.farm_area),
                            farm_cultivation_process = farm.farm_cultivation_process,
                            )
        form = AddFarmForm(obj=myFarm)               # CREATE WTForm FORM

    # print(type(form.farm_coordinates.data))
    # this is a string

    if form.validate_on_submit():   # IF request.methiod == 'POST'
        # USER OBJS
        user_id = current_user.get_id()

        # FARM OBJS
        farm_name = form.farm_name.data
        farm_location = form.farm_location.data
        # farm_coordinates = form.farm_coordinates.data


        # Calculate area*****************:


        farm_area = form.farm_area.data
        # farm_area = 1.0
        farm_cultivation_process = form.farm_cultivation_process.data

        # FARM OBJS TO DB
        if current_user.welcome.add_farm:
            print(current_user.welcome.add_farm)
            farm.farm_name = form.farm_name.data
            farm.farm_location = form.farm_location.data
            # farm.farm_coordinates = form.farm_coordinates.data
            farm.farm_area = m2_to_cm2(form.farm_area.data)
            farm.farm_cultivation_process = form.farm_cultivation_process.data
            farm._default = False
            flash('''You just re-created farm: {}
                        located: {}
                        with an area: {} m2
                        growing: {}ally'''.format(farm_name, farm_location, farm_area, farm_cultivation_process))
        else:
            farm = Farm(    user_id=user_id,
                            farm_name=farm_name,
                            farm_location=farm_location,
                            # farm_coordinates=farm_coordinates,
                            farm_area=m2_to_cm2(farm_area),
                            farm_cultivation_process=farm_cultivation_process,
                            _default=False)
            # DB COMMANDS
            db.session.add(farm)
            flash('''You just created farm: {}
                        located: {}
                        with an area: {} m2
                        growing: {}ally'''.format(farm_name, farm_location, farm_area, farm_cultivation_process))

        # DB COMMANDS
        current_user.welcome.add_farm = True
        db.session.commit()
        # OBJS SAVE ON SESSION
         # ADD SESSION OBJS
        farm_id = farm.id
        session['welcome'].update({'user_id': user_id,
                                'farm_id':farm_id,
                                'farm_name':farm_name,
                                'farm_location':farm_location,
                                # 'farm_coordinates': farm_coordinates,
                                'farm_area':farm_area,
                                'farm_cultivation_process':farm_cultivation_process})
        session.modified = True
        print("POST Successful")

        # DEAFULT FARM
        if current_user.farms.count() == 1: # if first time and first farm, set it as the default one
            print('Farm default nummer {} was added and type {}'.format(farm_id, type(farm_id)))
            current_user.default_farm_id = farm_id
            farm._default = True
            db.session.commit()

        # SUCESS AND REDIRECT TO NEXT STEP
        return redirect(url_for('welcome.add_soil_test'))
    return render_template('welcome/add_farm.html', form=form)


###################
# SET FIELD
###################

@welcome.route('/add-crop', methods=['GET', 'POST'])
@login_required
def add_crop():

    if 'welcome' not in session:
        session['welcome'] = dict()
        session.modified = True

    if not session['welcome']['user_id']:
        session['welcome'].update({'user_id': current_user.id})
        session.modified = True

    if not session['welcome']['farm_id']:
        only_farm_id = current_user.farms.first().id
        session['welcome'].update({'farm_id': only_farm_id})
        session.modified = True

    form = AddCropForm()              # CREATE WTForm FORM
    crop_choices = Crop.query.all()
    form.field_cultivation_crop.choices = [ (crop.id,  str.capitalize(crop._name)) for crop in crop_choices ]
    form.field_cultivation_crop.choices.insert(0, ('0' ,'Choose:'))
    if form.validate_on_submit():   # IF request.methiod == 'POST'
        # USER OBJS
        user = User.query.filter_by(id = session['welcome']['user_id']).first()
        farm = user.farms.filter_by(id = session['welcome']['farm_id']).first()

        # FIELD OBJS
        crop = Crop.query.filter_by(id = form.field_cultivation_crop.data).first()
        field_name = crop._name
        field_cultivation_area = form.field_cultivation_area.data
        field_cultivation_start_date = form.field_cultivation_start_date.data
        field_cultivation_state = form.field_cultivation_state.data
        field_cultivation_type = form.field_cultivation_type.data



        def m2_to_cm2(m2):
            return m2 * 10000

        def num_plants():
            area_in_cm2 = m2_to_cm2(field_cultivation_area) # cm2
            distance_rows_and_columns = sqrt(area_in_cm2) # cm. since we receive an area instead of a shape, we assumed is perfect square
            num_of_rows = (floor(distance_rows_and_columns / crop._space_x))/2 #
            num_of_cols = (floor(distance_rows_and_columns / crop._space_y))/2 # since space of plant and space for walk is the same DIVIDE by 2
            num_of_plants = num_of_rows * num_of_cols
            return num_of_plants

        # Calculated vars
        field_cultivation_finish_date = field_cultivation_start_date + timedelta(crop._dtg + crop._dtm) # datetime
        field_num_plants = num_plants() # number Integer
        field_projected_yield = crop._yield * field_num_plants # gr
        field_current_yield = 0
        field_water_required_day = field_num_plants * crop._water

        print('''finish date: {}
                 num plants: {} #
                 project yield: {} gr
                 water per day {} ml'''.format(field_cultivation_finish_date, field_num_plants, field_projected_yield, field_water_required_day))


        # FIELD OBJS TO DB
        field = Field(  field_name = field_name,
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
        current_user.completed_welcome = True # sets flag for user to have completed the welcome phase
        print('user.completed_welcome is ' + str(user.completed_welcome))
        current_user.welcome.add_field = True
        db.session.add(field)
        db.session.commit()

        # DEAFULT AGRIMODULE SYSTEM
        if current_user.farms.count() == 1 and current_user.farms.first().fields.count() == 1 and current_user.agrimodules.count() > 0: # if first time and first field, set it as the default one
            print('Field default agrimodule system nummer {} was added and type {}'.format(field.id, type(field.id)))
            agrimodule = current_user.agrimodules.first()
            agrimodule.field_id = field.id
            db.session.commit()

        #SUCESS AND REDIRECT TO DASHBOARD
        flash('You just created a {} in your {}'.format(field_name, farm.farm_name))
        del session['welcome']     # ERASE SESSION OBJS
        return redirect(url_for('login_check.index'))


    return render_template('welcome/add_crop.html', form=form)
