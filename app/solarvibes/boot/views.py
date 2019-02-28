from flask import Blueprint, redirect, url_for

boot = Blueprint(
    'boot',
    __name__
)

#############################
# BOOT INDEX
#############################
@boot.route('/', methods=['GET'])
# @login_required
def index():
    return redirect(url_for('site.index'))
