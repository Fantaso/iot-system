from flask import Blueprint, render_template, redirect, url_for, flash
from solarvibes.models import User, Agripump, Agrimodule, Field
from flask_login import current_user
from flask_security import login_required

crop_planning_bp = Blueprint(
    'crop_planning_bp',
    __name__,
    template_folder="templates"
)


##################
# CROP PLANNING
##################
@crop_planning_bp.route('/', methods=['GET'])
@login_required
def show():
    pass
