from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, NumberRange



class FarmForm(FlaskForm):
    farm_name                   = StringField('Farm name', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    farm_location               = StringField('Farm location', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    farm_area                   = FloatField('Farm Cultivation Area', validators=[DataRequired(), NumberRange(min=1, max=5000, message='Area between 1 and 5000 m2')])
    farm_cultivation_process    = SelectField('Farm Cultivation Process', validators=[DataRequired()], choices=[('Organic','Organic'),('Chemical','Chemical')])


class FieldForm(FlaskForm):
    field_name                    = StringField(label='Field name', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    field_cultivation_area       = FloatField(label='Field Cultivation Area', validators=[DataRequired(), NumberRange(min=1, max=5000, message='Cultivation area should be maximum as big as your farm')],render_kw={"placeholder":"500.50"})
    field_cultivation_crop        = SelectField(label='Cultivation Crop', validators=[DataRequired()], coerce = int)
    field_cultivation_start_date  = DateField(label='Cultivation Start Date', format='%d %B, %Y', validators=[DataRequired()])
    field_cultivation_state       = SelectField(label='Cultivation State', validators=[DataRequired()], choices=[('new','New'),('already growing','Already Growing')])
    field_cultivation_type        = SelectField(label='Cultivation Type', validators=[DataRequired()], choices=[('mono','Mono'), ('mix','Mix'), ('multi','Multi')])

class PreNewCropForm:
    def __init__(self, field_cultivation_area, field_cultivation_start_date, field_cultivation_state, field_cultivation_type):
        self.field_cultivation_area          = field_cultivation_area
        self.field_cultivation_start_date    = field_cultivation_start_date
        self.field_cultivation_state         = field_cultivation_state
        self.field_cultivation_type          = field_cultivation_type

class PreDateNewCropForm:
    def __init__(self, field_cultivation_start_date):
        self.field_cultivation_start_date = field_cultivation_start_date

class NewCropForm(FlaskForm):
    farm_choices                  = SelectField(label='Choose Farm', validators=[DataRequired()], coerce = int)
    field_cultivation_area        = FloatField(label='Field Cultivation Area', validators=[DataRequired()], render_kw={'placeholder':'Field area should not exceed the available land on your farm'})
    field_cultivation_crop        = SelectField(label='Cultivation Crop', validators=[DataRequired()], coerce = int)
    field_cultivation_start_date  = DateField(label='Cultivation Start Date', format='%d %B, %Y', validators=[DataRequired()])
    field_cultivation_state       = SelectField(label='Cultivation State', validators=[DataRequired()], choices=[('new','New'),('already growing','Already Growing')])
    field_cultivation_type        = SelectField(label='Cultivation Type', validators=[DataRequired()], choices=[('mono','Mono'), ('mix','Mix'), ('multi','Multi')])

class PreEditFarmForm:
    def __init__(self, farm_name, farm_location, farm_area, farm_cultivation_process):
        self.farm_name                  = farm_name
        self.farm_location              = farm_location
        self.farm_area                  = farm_area
        self.farm_cultivation_process   = farm_cultivation_process

class EditFarmForm(FlaskForm):
    farm_name                   = StringField('Farm name', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    farm_location               = StringField('Farm location', validators=[DataRequired(), Length(min=2, max=30, message='''Your name needs at least 2 characters.''')])
    farm_area                   = FloatField('Farm Cultivation Area', validators=[DataRequired(), NumberRange(min=1, max=5000, message='Area between 1 and 5000 m2')])
    farm_cultivation_process    = SelectField('Farm Cultivation Process', validators=[DataRequired()], choices=[('Organic','Organic'),('Chemical','Chemical')])
