from solarvibes import db
from sqlalchemy.sql import func
from flask_security import UserMixin, RoleMixin


#############################
#############################
# USER MODELS FLASK-SECURITY
#############################
#############################



#############################
#############################
# FARMS AND AGRIMODULE MODELS
#############################
#############################

class Farm(db.Model):
    """Farms Models for Users to create. One User can created as many farms as he wants"""
    __tablename__ = 'farm'
    id = db.Column(db.Integer, primary_key=True)
    farm_name = db.Column(db.String(25), unique=True, nullable=False)
    farm_location = db.Column(db.String(20))
    farm_coordinates = db.Column(db.String(3000))
    farm_area = db.Column(db.Float(precision=2))
    farm_cultivation_process = db.Column(db.String(20))

    # RELATIONSHIP
    # USER[1]-FARM[M]
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # FARM[1]-FIELD[M]
    fields = db.relationship('Field', backref='farm', lazy='dynamic')
    soil_tests = db.relationship('SoilTest', backref='farm', lazy='dynamic')
    water_tests = db.relationship('WaterTest', backref='farm', lazy='dynamic')

    _default = db.Column(db.Boolean)
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<farm {}>'.format(self.farm_name)

crops_field = db.Table('crops_field',
    db.Column('field_id', db.Integer, db.ForeignKey('field.id')),
    db.Column('crop_id', db.Integer, db.ForeignKey('crop.id')))

class SoilTest(db.Model):

    __tablename__ = 'soiltest'
    id = db.Column(db.Integer, primary_key=True)
    soil_ph = db.Column(db.Float(precision=2))
    soil_ec = db.Column(db.Float(precision=2))
    soil_organic_carbon = db.Column(db.Float(precision=2))
    soil_nitrogen = db.Column(db.Float(precision=2))
    soil_p205 = db.Column(db.Float(precision=2))
    soil_k20 = db.Column(db.Float(precision=2))

    # FARM[1]-TEST[M]
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
      return '<Soil Test {}>'.format(self.id)

class WaterTest(db.Model):

    __tablename__ = 'watertest'
    id = db.Column(db.Integer, primary_key=True)
    water_ph = db.Column(db.Float(precision=2))
    water_ec = db.Column(db.Float(precision=2))
    water_bicarbonates = db.Column(db.Float(precision=2))
    water_carbonates = db.Column(db.Float(precision=2))
    water_potasium = db.Column(db.Float(precision=2))
    water_sulphate = db.Column(db.Float(precision=2))

    # FARM[1]-TEST[M]
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
      return '<Water Test {}>'.format(self.id)

class Field(db.Model):
    """Fields that can exist inside the Farm.Model. One Farm can have as many Fields within for different crops to be cultivated, being limited by the size of the Farm"""
    __tablename__ = 'field'
    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(25), nullable=False)
    field_cultivation_area = db.Column(db.Float(precision=2))
    field_cultivation_start_date = db.Column(db.DateTime(timezone=True))
    field_cultivation_finish_date = db.Column(db.DateTime(timezone=True))
    field_current_yield = db.Column(db.Float(precision=2))
    field_projected_yield = db.Column(db.Float(precision=2))
    field_cultivation_state = db.Column(db.String(20))
    field_cultivation_type = db.Column(db.String(5))

    field_num_plants = db.Column(db.Integer)
    field_spacing_topology = db.Column(db.String(20))
    field_water_required_day = db.Column(db.Integer)
    # field_ = db.Column(db.Float)

    # RELATIONSHIP TO BE ADDED
    agrimodule = db.relationship('Agrimodule', uselist=False, backref='field')
        # FIELD[1]-AGRIMODULE[1]

    # RELATIONSHIP
    # FIELD[M]-CROP[M]
    crops = db.relationship('Crop', secondary='crops_field', backref='field', lazy='dynamic')
    # FARM[1]-FIELD[M]
    farm_id = db.Column(db.Integer, db.ForeignKey('farm.id'))

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<field {}>'.format(self.field_name)

# calculated everyday per day
class DailyFieldInput(db.Model):
    __tablename__ = 'dailyfieldinput'
    # automaticv values
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now()) # day and time
    # from agripump schedule
    daily_pump_on_time = db.Column(db.Float) # minutes
    # calculated values
    daily_water = db.Column(db.Float) # ml
    daily_energy = db.Column(db.Float) # Wm
    # from agrimodule
    avg_air_radiation = db.Column(db.Float) # w/cm2
    avg_air_temperature = db.Column(db.Float) # C
    avg_air_humidity = db.Column(db.Float) # % RH
    avg_air_pressure = db.Column(db.Float) # kPa
    avg_soil_temperature = db.Column(db.Float) # C
    avg_soil_humidity = db.Column(db.Float) # %
    avg_soil_ph = db.Column(db.Float)
    avg_soil_nutrients = db.Column(db.Float) # siemens
        # percentages
    avg_air_radiation_percentage = db.Column(db.Float) # w/cm2
    avg_air_temperature_percentage = db.Column(db.Float) # C
    avg_air_humidity_percentage = db.Column(db.Float) # % RH
    avg_air_pressure_percentage = db.Column(db.Float) # kPa
    avg_soil_temperature_percentage = db.Column(db.Float) # C
    avg_soil_humidity_percentage = db.Column(db.Float) # %
    avg_soil_ph_percentage = db.Column(db.Float)
    avg_soil_nutrients_percentage = db.Column(db.Float) # siemens

    # from weather forecast API
    avg_rain = db.Column(db.Float)
    avg_wind = db.Column(db.Float)
    avg_wind_direction = db.Column(db.Float)

    def __repr__(self):
        return '<dailyfieldinput {}>'.format(self.id)
class CropImage(db.Model):
    _tablename_ = 'cropimages'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), unique=True)

class Crop(db.Model):
    '''The crop database reference from farmers or Users.model that can be be cultivated in the Field.Model'''
    __tablename__ = 'crop'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(25), unique=True, nullable=False)
    _variety = db.Column(db.String(25))
    _family = db.Column(db.String(25))
    _yield = db.Column(db.Float(precision=2))
    _space_x = db.Column(db.Float(precision=2))
    _space_y = db.Column(db.Float(precision=2))
    _space_z = db.Column(db.Float(precision=2))
    _density = db.Column(db.Float(precision=2))
    image = db.Column(db.String(200), unique=True)
    # FRUITS EACH PLANT
    _fruit_quantity = db.Column(db.Integer)
    _fruit_size = db.Column(db.Float(precision=2))
    _fruit_weight = db.Column(db.Float(precision=2))
    # RESOURCES REQUIRED
    _water = db.Column(db.Float(precision=4))
    _nutrient = db.Column(db.Float(precision=4))
    _radiation = db.Column(db.Float(precision=4))
    # CYCLE
    _dtg = db.Column(db.Integer)
    _dtm = db.Column(db.Integer)
    # REQUIREMENTS
    # SOIL
    _soil_ph_min = db.Column(db.Float(precision=2))
    _soil_ph_opt = db.Column(db.Float(precision=2))
    _soil_ph_max = db.Column(db.Float(precision=2))

    _soil_temp_min = db.Column(db.Float(precision=2))
    _soil_temp_opt = db.Column(db.Float(precision=2))
    _soil_temp_max = db.Column(db.Float(precision=2))

    _soil_humi_min = db.Column(db.Float(precision=2))
    _soil_humi_opt = db.Column(db.Float(precision=2))
    _soil_humi_max = db.Column(db.Float(precision=2))

    _soil_nutrient_min = db.Column(db.Float(precision=2))
    _soil_nutrient_opt = db.Column(db.Float(precision=2))
    _soil_nutrient_max = db.Column(db.Float(precision=2))
    # AIR
    _air_temp_min = db.Column(db.Float(precision=2))
    _air_temp_opt = db.Column(db.Float(precision=2))
    _air_temp_max = db.Column(db.Float(precision=2))

    _air_humi_min = db.Column(db.Float(precision=2))
    _air_humi_opt = db.Column(db.Float(precision=2))
    _air_humi_max = db.Column(db.Float(precision=2))
    # WATER
    _water_needed = db.Column(db.Integer) # not reuired is already declared some lines before _water

    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<crop {}>'.format(self._name)

#  crop planning db model
class CropPlanning(db.Model):
    __tablename__ = 'cropplanning'
    id = db.Column(db.Integer, primary_key = True)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Integer) # name of the task
    description = db.Column(db.String(2000)) # description of the task (brief overview)
    freq = db.Column(db.String(20)) # frequency of the task (weekly, bi-weekly etc)
    duration = db.Column(db.Integer) # hours
    man_power = db.Column(db.Integer) # number of man power needed

# farm management system model
class Pump(db.Model):
    """pump database used for each field or each agripump whichi is installed in the farm. one farm can ahve as many pump the want as long as the have an agripump for it"""
    __tablename__ = 'pump'
    id = db.Column(db.Integer, primary_key=True)
    pump_name = db.Column(db.String(30))
    pump_brand = db.Column(db.String(25))
    pump_flow_rate = db.Column(db.Float(precision=2), nullable=False)
    pump_head = db.Column(db.Float(presicion=2), nullable=False)
    pump_watts = db.Column(db.Float(precision=2), nullable=False)

    # RELATIONSHIP
    # USER[1]-PUMP[M]
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # PUMP[1]-AGRIPUMP
    agripumps = db.relationship('Agripump', backref='pump', lazy='dynamic')

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<pump {}>'.format(self.pump_brand)

class AgrimoduleList(db.Model):
    __tablename__ = 'agrimodulelist'
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(100), unique = True, nullable = False)
    type = db.Column(db.String(10), nullable = False) # agrimodule, agrisensor, agripump

    has_user_registered = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)
    has_agrimodule_registered = db.Column(db.Boolean)

class AgrisensorList(db.Model):
    __tablename__ = 'agrisensorlist'
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(100), unique = True, nullable = False)
    type = db.Column(db.String(10), nullable = False) # agrimodule, agrisensor, agripump

    has_user_registered = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)
    has_agrimodule_registered = db.Column(db.Boolean)

class AgripumpList(db.Model):
    __tablename__ = 'agripumplist'
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(100), unique = True, nullable = False)
    type = db.Column(db.String(10), nullable = False) # agrimodule, agrisensor, agripump

    has_user_registered = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)
    has_agrimodule_registered = db.Column(db.Boolean)

class WelcomeLog(db.Model):
    __tablename__ = 'welcome'
    id = db.Column(db.Integer, primary_key=True)
    add_agrisys = db.Column(db.Boolean)
    install_agrisys = db.Column(db.Boolean)
    add_pump = db.Column(db.Boolean)
    add_farm = db.Column(db.Boolean)
    add_field = db.Column(db.Boolean)
    add_soil_test = db.Column(db.Boolean)
    add_water_test = db.Column(db.Boolean)
    # WELCOME[1]-USER[1]
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<welcomelog {}>'.format(self.id)


class Agrimodule(db.Model):
    """Each agrimodule smart system is unique and has am agrimodule an agripump and maybe agresiensor and other agripumps depending on the complaexity of the farm
    and can be added to any user any farm with a unique identuifier which can connect the data being sent to server to an specific User.Model/Field.Model
    Each agrimodule"""
    __tablename__ = 'agrimodules'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    identifier = db.Column(db.String(100), unique=True, nullable=False)
    lat = db.Column(db.Float(precision=8))
    lon = db.Column(db.Float(precision=8))
    batt_status = db.Column(db.Integer)
    public_id = db.Column(db.String(200))
    mac = db.Column(db.String(400))


    # RELATIONSHIP
        # USER[1]-agrimodule[M]
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        # FIELD[1]-agrimodule[1]
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'))
        # AGRIMODULE[1]-MEASUREMENT[M]
    measurements = db.relationship('Measurement', backref='agrimodule', lazy='dynamic')
        # AGRIMODULE[1]-AGRISENSOR[M]
    agrisensors = db.relationship('Agrisensor', backref='agrimodule', lazy='dynamic')
        # AGRIMODULE[1]-AGRIPUMP[M]
    agripumps = db.relationship('Agripump', backref='agrimodule', lazy='dynamic')

    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<agrimodule {}>'.format(self.identifier)



class Agrisensor(db.Model):
    """each agrimodule has a different table where all data that is measured by agrimodule is saved in this model"""
    __tablename__ = 'agrisensors'

    id = db.Column(db.Integer, primary_key=True)

    identifier = db.Column(db.String(50), unique=True)
    lat = db.Column(db.Float(precision=8))
    lon = db.Column(db.Float(precision=8))
    batt_status = db.Column(db.Integer)


    # RELATIONSHIP
    # agrimodule[1]-AGRIMODULE[M]
    agrimodule_id = db.Column(db.Integer, db.ForeignKey('agrimodules.id'))
    # AGRIMODULE[1]-MEASUREMENT[M]
    measurements = db.relationship('Measurement', backref='agrisensor', lazy='dynamic')

    # SETTINGS
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<agrisensor {}>'.format(self.identifier)

class Measurement(db.Model):
    __tablename__ = 'measurements'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True))

    soil_ph = db.Column(db.Float(precision=4))
    soil_nutrient = db.Column(db.Float(precision=4))
    soil_temp = db.Column(db.Float(precision=4))
    soil_humi = db.Column(db.Float(precision=4))

    air_temp = db.Column(db.Float(precision=4))
    air_humi = db.Column(db.Float(precision=4))
    air_pres = db.Column(db.Float(precision=4))
    solar_radiation = db.Column(db.Float(precision=4))

    batt_status = db.Column(db.Integer)
    lat = db.Column(db.Float(precision=8))
    lon = db.Column(db.Float(precision=8))


    # REALTIONSHIPS
    # AGRIMODULE[1]-MEASUREMENT[M]
    agrimodule_id = db.Column(db.Integer, db.ForeignKey('agrimodules.id'))
    # AGRIPUMP[1]-MEASUREMENT[M]
    agripump_id = db.Column(db.Integer, db.ForeignKey('agrisensors.id'))

    def __repr__(self):
        return '<measurement {}>'.format(self.id)


class Agripump(db.Model):
    """pump schedule for each farm and agripump, it requires to know which Pump.Model is used in order to make the calculations"""
    __tablename__ = 'agripumps'

    id = db.Column(db.Integer, primary_key=True)

    identifier = db.Column(db.String(50), unique=True)
    lat = db.Column(db.Float(precision=8))
    lon = db.Column(db.Float(precision=8))
    status = db.Column(db.Boolean)


    # REQUIREMENTS
    _daily_water = db.Column(db.Float(precision=3))
    _date = db.Column(db.DateTime(timezone=True))
    # SCHEDULE IN MINUTES
    # _00_HOUR = db.Column(db.Float(precision=1))
    # _01_HOUR = db.Column(db.Float(precision=1))
    # _02_HOUR = db.Column(db.Float(precision=1))
    # _03_HOUR = db.Column(db.Float(precision=1))
    # _04_HOUR = db.Column(db.Float(precision=1))
    # _05_HOUR = db.Column(db.Float(precision=1))
    # _06_HOUR = db.Column(db.Float(precision=1))
    # _07_HOUR = db.Column(db.Float(precision=1))

    # _08_HOUR = db.Column(db.Float(precision=1))
    # _09_HOUR = db.Column(db.Float(precision=1))
    # _10_HOUR = db.Column(db.Float(precision=1))
    # _11_HOUR = db.Column(db.Float(precision=1))
    # _12_HOUR = db.Column(db.Float(precision=1))
    # _13_HOUR = db.Column(db.Float(precision=1))
    # _14_HOUR = db.Column(db.Float(precision=1))
    # _15_HOUR = db.Column(db.Float(precision=1))
    # _16_HOUR = db.Column(db.Float(precision=1))
    # _17_HOUR = db.Column(db.Float(precision=1))

    # _18_HOUR = db.Column(db.Float(precision=1))
    # _19_HOUR = db.Column(db.Float(precision=1))
    # _20_HOUR = db.Column(db.Float(precision=1))
    # _21_HOUR = db.Column(db.Float(precision=1))
    # _22_HOUR = db.Column(db.Float(precision=1))
    # _23_HOUR = db.Column(db.Float(precision=1))


    # TIME USAGE
    start_hour_per_day = db.Column(db.Integer)
    qty_hour_per_day = db.Column(db.Integer)

    time_per_hour = db.Column(db.Float)
    time_per_day = db.Column(db.Float)
    time_per_cycle = db.Column(db.Float)
    # WATER USAGE
    water_per_hour = db.Column(db.Integer)
    water_per_day = db.Column(db.Integer)
    water_per_cycle = db.Column(db.Integer)
    # ENERGY USAGE
    energy_per_hour = db.Column(db.Integer)
    energy_per_day = db.Column(db.Integer)
    energy_per_cycle = db.Column(db.Integer)


    # REALTIONSHIPS
    # AGRIMODULE[1]-AGRIPUMP[M]
    agrimodule_id = db.Column(db.Integer, db.ForeignKey('agrimodules.id'))
    # PUMP[1]-AGRIPUMP[M]
    pump_id = db.Column(db.Integer, db.ForeignKey('pump.id'))


    # SETTINGS
    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return '<agripump {}>'.format(self.identifier)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    birthday = db.Column(db.DateTime(timezone=True), nullable=True)
    mobile = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(50))
    zipcode = db.Column(db.Integer)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    email_rec = db.Column(db.String(50))
    image = db.Column(db.String(200))

    last_login_at = db.Column(db.DateTime(timezone=True))
    current_login_at = db.Column(db.DateTime(timezone=True))
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)

    active = db.Column(db.Boolean(), nullable=True)
    confirmed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    default_farm_id = db.Column(db.Integer, unique=True)
    completed_welcome = db.Column(db.Boolean)

    # RELATIONSHIP
    # USER[1]-FARM[M]
    farms = db.relationship('Farm', backref='user', lazy='dynamic')
    # USER[1]-AGRIMODULE[M]
    agrimodules = db.relationship('Agrimodule', backref='user', lazy='dynamic')
    # USER[1]-PUMP[M]
    pumps = db.relationship('Pump', backref='user', lazy='dynamic')
    # USER[1]-WELCOME[1]
    welcome = db.relationship('WelcomeLog', uselist=False, backref='user')


    _time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    _time_updated = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())



    def __repr__(self):
        return '<user {}>'.format(self.email)
