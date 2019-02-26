from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Optional

# If the FloatField is optional but needs validation
class ConditionalFloatValidation(object):
    def __init__(self, min, max, message):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
      data = field.data
      if (
        data is not None
        and (data < self.min or data > self.max)
      ):
        raise ValidationError(self.message)

class PreAddFarmForm:
    def __init__(self, farm_name, farm_location, farm_area, farm_cultivation_process):
        self.farm_name                   = farm_name
        self.farm_location               = farm_location
        # self.farm_location_coordinates   = farm_location_coordinates
        # self.farm_coordinates            = farm_coordinates
        self.farm_area                   = farm_area
        self.farm_cultivation_process    = farm_cultivation_process

class AddFarmForm(FlaskForm):
    farm_name                   = StringField('Farm name', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    farm_location               = StringField('Farm location', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    # farm_location_coordinates   = HiddenField('', validators=[DataRequired()])
    # farm_coordinates            = HiddenField('', validators=[DataRequired()])
    farm_area                   = FloatField('Farm Cultivation Area', validators=[DataRequired(), NumberRange(min=1, max=5000, message='Area between 1 and 5000 m2')])
    farm_cultivation_process    = SelectField('Farm Cultivation Process', validators=[DataRequired()], choices=[('Organic','Organic'),('Chemical','Chemical')])

class PreAddSoilTestForm:
    def __init__(self, soil_ph, soil_ec, soil_organic_carbon, soil_nitrogen, soil_p205, soil_k20):
        self.soil_ph              = soil_ph
        self.soil_ec              = soil_ec
        self.soil_organic_carbon  = soil_organic_carbon
        self.soil_nitrogen        = soil_nitrogen
        self.soil_p205            = soil_p205
        self.soil_k20             = soil_k20

class AddSoilTestForm(FlaskForm):
    soil_ph             = FloatField(label='pH', validators=[ConditionalFloatValidation(min=0, max=14.0, message='pH should be between 1 to 14'), Optional()])
    soil_ec             = FloatField(label='EC (ds/m)', validators=[ConditionalFloatValidation(min=0, max=20.0, message='EC should be between 1 to 20 ds/m'), Optional()])
    soil_organic_carbon = FloatField(label='Organic Carbon (%)', validators=[ConditionalFloatValidation(min=0, max=4, message='Orgnic Carbon should be between 0 to 4%'), Optional()])
    soil_nitrogen       = FloatField(label='Available nitrogen (kg/ha)')
    soil_p205           = FloatField(label='Available P205 (kg/ha)')
    soil_k20            = FloatField(label='Available K20 (kg/ha)')

class PreAddWaterTestForm:
    def __init__(self, water_ph, water_ec, water_bicarbonates, water_carbonates, water_potasium, water_sulphate):
        self.water_ph              = water_ph
        self.water_ec              = water_ec
        self.water_bicarbonates    = water_bicarbonates
        self.water_carbonates      = water_carbonates
        self.water_potasium        = water_potasium
        self.water_sulphate        = water_sulphate

class AddWaterTestForm(FlaskForm):
    water_ph             = FloatField(label='pH', validators=[ConditionalFloatValidation(min=0.0, max=14.0, message='pH should be between 1 to 14'), Optional()])
    water_ec             = FloatField(label='EC (ds/m)', validators=[ConditionalFloatValidation(min=0.0, max=20.0, message='EC should be between 1 to 20 ds/m'), Optional()])
    water_bicarbonates   = FloatField(label='Bicarbonates')
    water_carbonates     = FloatField(label='Carbonates')
    water_potasium       = FloatField(label='Potasium')
    water_sulphate       = FloatField(label='Sulphate')

class PreAddCropForm:
    def __init__(self, field_cultivation_area, field_cultivation_crop, field_cultivation_start_date, field_cultivation_state, field_cultivation_type):
        # self.field_name                    = field_name
        self.field_cultivation_area        = field_cultivation_area
        self.field_cultivation_crop        = field_cultivation_crop
        self.field_cultivation_start_date  = field_cultivation_start_date
        self.field_cultivation_state       = field_cultivation_state
        self.field_cultivation_type        = field_cultivation_type

class AddCropForm(FlaskForm):
    # field_name                    = StringField(label='Field name', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    field_cultivation_area        = FloatField(label='Field Cultivation Area', validators=[DataRequired(), NumberRange(min=1, max=5000, message='Cultivation area should be maximum as big as your farm')],render_kw={"placeholder":"500.50"})
    field_cultivation_crop        = SelectField(label='Cultivation Crop', validators=[DataRequired()], coerce = int)
    field_cultivation_start_date  = DateField(label='Cultivation Start Date', format='%d %B, %Y', validators=[DataRequired()])
    field_cultivation_state       = SelectField(label='Cultivation State', validators=[DataRequired()], choices=[('new','New'),('already growing','Already Growing')])
    field_cultivation_type        = SelectField(label='Cultivation Type', validators=[DataRequired()], choices=[('mono','Mono'), ('mix','Mix'), ('multi','Multi')])

class PreAddAgrisysForm:
    def __init__(self, agrimodule_name, agrimodule_identifier):
        self.agrimodule_name              = agrimodule_name
        self.agrimodule_identifier        = agrimodule_identifier

class AddAgrisysForm(FlaskForm):
    agrimodule_name              = StringField('Agrimodule Name', validators=[DataRequired(), Length(min=2, max=20, message='Give it a name for sanity MAX 30.')])
    agrimodule_identifier        = StringField('Agrimodule Code', validators=[DataRequired(), Length(min=2, max=30, message='Your agrimodule system identifier is in the back of your agrimodule.')])

class PreInstallAgrisysForm:
    def __init__(self, agm_lat, agm_lon, ags_lat, ags_lon, agp_lat, agp_lon):
        self.agm_lat        = agm_lat
        self.agm_lon        = agm_lon
        self.ags_lat        = ags_lat
        self.ags_lon        = ags_lon
        self.agp_lat        = agp_lat
        self.agp_lon        = agp_lon

class InstallAgrisysForm(FlaskForm):
    agm_lat                 = FloatField('Agrimodule latitude location',       validators=[DataRequired(), NumberRange(min=-90, max=90, message='write the lat coordinates')])
    agm_lon                 = FloatField('Agrimodule longitude location',      validators=[DataRequired(), NumberRange(min=-180, max=180, message='write the lon coordinates')])
    ags_lat                 = FloatField('Agrisensor latitude location',       validators=[DataRequired(), NumberRange(min=-90, max=90, message='write the lat coordinates')])
    ags_lon                 = FloatField('Agrisensor longitude location',      validators=[DataRequired(), NumberRange(min=-180, max=180, message='write the lon coordinates')])
    agp_lat                 = FloatField('Agripump latitude location',         validators=[DataRequired(), NumberRange(min=-90, max=90, message='write the lat coordinates')])
    agp_lon                 = FloatField('Agripump longitude location',        validators=[DataRequired(), NumberRange(min=-180, max=180, message='write the lon coordinates')])

class PreAddPumpForm:
    def __init__(self, pump_name, pump_brand, pump_flow_rate, pump_head, pump_watts):
        self.pump_name       = pump_name
        self.pump_brand      = pump_brand
        self.pump_flow_rate  = pump_flow_rate
        self.pump_head       = pump_head
        self.pump_watts      = pump_watts

class AddPumpForm(FlaskForm):
    pump_name               = StringField('Pump name',                              validators=[DataRequired(), Length(min=2, max=30, message='Give it a name for sanity MAX 30.')])
    pump_brand              = StringField('Pump brand',                             validators=[DataRequired(), Length(min=2, max=30, message='Your pump supplier or brand name')])
    pump_flow_rate          = FloatField('Pump flow rate (liters per sec)',         validators=[DataRequired(), NumberRange(min=1, max=500, message="Your pump's water capacity or water turn over")])
    pump_head               = FloatField('Pump head (meters)',                      validators=[DataRequired(), NumberRange(min=1, max=500, message="Your pump's max head pressure or height power")])
    pump_watts              = FloatField('Pump power consumption (kilo Watts)',     validators=[DataRequired(), NumberRange(max=1000, message="Your pump's wattage consumption")])
