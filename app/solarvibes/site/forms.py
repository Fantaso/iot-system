from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

# WEBSITE FORMS
# Templates
class EmailForm(FlaskForm):
	email 	= StringField('Email', validators=[DataRequired(), Length(min=5, max=30, message=None), Email()])

class EmailAndTextForm(EmailForm):
	msg     = TextAreaField('Message', validators=[DataRequired(), Length(min=-1, max=1000, message='Maximum characters: 1000')])

class ContactUsForm(EmailAndTextForm):
    name 	= StringField(label='Fullname', validators=[DataRequired(), Length(min=3, max=30, message=None)])
    phone 	= StringField('Phone', validators=[DataRequired(), Length(min=7, max=30, message=None)])
