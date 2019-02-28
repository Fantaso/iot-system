from flask import Blueprint, redirect, url_for

app = Blueprint(
    'app',
    __name__,
)

#############################
# BOOT INDEX
#############################
@app.route('/', methods=['GET'])
# @login_required
def index():
    return redirect(url_for('login_check.index'))
