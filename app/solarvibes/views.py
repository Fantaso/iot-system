from flask import current_app, render_template, session, request, redirect, url_for, flash, jsonify

from solarvibes import db

from flask_uploads import UploadSet, configure_uploads, IMAGES

from datetime import datetime, timedelta
from math import sqrt, floor

from flask_login import current_user

from flask_security import login_required

from solarvibes.models import roles_users, Role, User, Farm, Field, DailyFieldInput, Crop, Pump, Agrimodule, Agrisensor, Measurement, Agripump


#############################
# SITE INDEX
#############################
@current_app.route('/', methods=['GET'])
# @login_required
def site_index():
    return redirect(url_for('login_check.index'))


#############################
# APP INDEX
#############################
@current_app.route('/app', methods=['GET'])
# @login_required
def app_index():
    return redirect(url_for('login_check.index'))


















##########################################################
##########################################################
# FARM VIEWS
##########################################################
##########################################################
##################
# USER WEATHER
##################
@current_app.route('/user/farm/weather', methods=['GET'])
@login_required
def user_weather():
    return render_template('user_weather.html')


##################
# USER ALERTS
##################
@current_app.route('/user/farm/alerts', methods=['GET', 'POST'])
@login_required
def user_alerts():
    return render_template('user_alerts.html')


##########################################################
##########################################################
# FARMER VIEWS
##########################################################
##########################################################
##################
# ALERTS
##################
@current_app.route('/user/farm/farmer/crop-planning', methods=['GET'])
@login_required
def user_crop_planning():
    return render_template('user_crop_planning.html')


##################
# CROP ANALYZER
##################
@current_app.route('/user/farm/farmer/crop-analyzer', methods=['GET'])
@login_required
def user_crop_analyzer():
    return render_template('user_crop_analyzer.html')


##################
# HEALTH ANALYZER
##################
@current_app.route('/user/farm/farmer/health-analyzer', methods=['GET'])
@login_required
def user_health_analyzer():
    return render_template('user_health_analyzer.html')


##################
# RESOURCES
##################
@current_app.route('/user/farm/farmer/resources', methods=['GET'])
@login_required
def user_resources():
    return render_template('user_resources.html')


##########################################################
##########################################################
# MARKET VIEWS
##########################################################
##########################################################
@current_app.route('/user/market', methods=['GET'])
@login_required
def user_market():
    return render_template('user_market.html')
