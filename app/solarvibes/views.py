from flask import render_template, session, request, redirect, url_for, flash, jsonify

from solarvibes import application, db

from flask_uploads import UploadSet, configure_uploads, IMAGES

from datetime import datetime, timedelta
from math import sqrt, floor

from flask_login import current_user

from flask_security import login_required

from solarvibes.models import roles_users, Role, User, Farm, Field, DailyFieldInput, Crop, Pump, Agrimodule, Agrisensor, Measurement, Agripump


#############################
# SITE INDEX
#############################
@application.route('/', methods=['GET'])
# @login_required
def site_index():
    return redirect(url_for('login_check.index'))


#############################
# APP INDEX
#############################
@application.route('/app', methods=['GET'])
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
@application.route('/user/farm/weather', methods=['GET'])
@login_required
def user_weather():
    return render_template('user_weather.html')


##################
# USER ALERTS
##################
@application.route('/user/farm/alerts', methods=['GET', 'POST'])
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
@application.route('/user/farm/farmer/crop-planning', methods=['GET'])
@login_required
def user_crop_planning():
    return render_template('user_crop_planning.html')


##################
# CROP ANALYZER
##################
@application.route('/user/farm/farmer/crop-analyzer', methods=['GET'])
@login_required
def user_crop_analyzer():
    return render_template('user_crop_analyzer.html')


##################
# HEALTH ANALYZER
##################
@application.route('/user/farm/farmer/health-analyzer', methods=['GET'])
@login_required
def user_health_analyzer():
    return render_template('user_health_analyzer.html')


##################
# RESOURCES
##################
@application.route('/user/farm/farmer/resources', methods=['GET'])
@login_required
def user_resources():
    return render_template('user_resources.html')


##########################################################
##########################################################
# MARKET VIEWS
##########################################################
##########################################################
@application.route('/user/market', methods=['GET'])
@login_required
def user_market():
    return render_template('user_market.html')
