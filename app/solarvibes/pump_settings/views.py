from flask import Blueprint, render_template, redirect, url_for, flash
from solarvibes import db
from solarvibes.pump_settings.forms import PreAddPumpForm, AddPumpForm
from solarvibes.models import Pump
from flask_login import current_user
from flask_security import login_required

pump_settings = Blueprint(
    'pump_settings',
    __name__,
    template_folder="templates"
)


###################
# USER ADD PUMP
###################
@pump_settings.route('/add-pump', methods=['GET', 'POST'])
@login_required
def add_pump():

    form = AddPumpForm()
    if form.validate_on_submit():

        def lps_to_mlpm(lps):
            return lps * (1000 * 60)
        def m_to_cm(m):
            return m * 100
        def kw_to_w(kw):
            return kw * 1000
        # ADD PUMP OBJS
        pump_name = form.pump_name.data
        pump_brand = form.pump_brand.data
        pump_flow_rate = lps_to_mlpm(form.pump_flow_rate.data)
        pump_head = m_to_cm(form.pump_head.data)
        pump_watts = kw_to_w(form.pump_watts.data)
        print(pump_brand)
        print(pump_flow_rate)
        print(pump_head)
        print(pump_watts)

        # OBJS TO DB
        pump = Pump(user = current_user, pump_name = pump_name, pump_brand = pump_brand, pump_flow_rate = pump_flow_rate, pump_head = pump_head, pump_watts = pump_watts)

        # DB COMMANDS
        db.session.add(pump)
        db.session.commit()

        # FLASH AND REDIRECT
        flash('''Your Pump brand: {}
                Flow rate: {} lps
                Head pressure: {} m
                Wattage: {} kW'''.format(form.pump_brand, form.pump_flow_rate.data, form.pump_head.data, form.pump_watts.data))
        return redirect(url_for('settings.index'))

    return render_template('pump_settings/add_pump.html', form=form)


###################
# USER EDIT PUMP
###################
@pump_settings.route('/edit-pump', methods=['GET', 'POST'])
@pump_settings.route('/edit-pump/<pump_id>', methods=['GET', 'POST'])
@login_required
def edit_pump(pump_id = 0):

    if int(pump_id) <= 0:
        flash('This Pump does not exist.')
        return redirect(url_for('settings.index'))

    def mlpm_to_lps(mlpm):
        return mlpm / (1000 * 60)
    def cm_to_m(cm):
        return cm / 100
    def w_to_kw(w):
        return w / 1000

    pump_to_edit = current_user.pumps.filter_by(id = pump_id).first()


    myPump = PreAddPumpForm(pump_name = pump_to_edit.pump_name, pump_brand = pump_to_edit.pump_brand, pump_flow_rate = mlpm_to_lps(pump_to_edit.pump_flow_rate), pump_head = cm_to_m(pump_to_edit.pump_head), pump_watts = w_to_kw(pump_to_edit.pump_watts))

    form = AddPumpForm(obj = myPump)
    if form.validate_on_submit():

        def lps_to_mlpm(lps):
            return lps * (1000 * 60)
        def m_to_cm(m):
            return m * 100
        def kw_to_w(kw):
            return kw * 1000
        # ADD PUMP OBJS
        pump_to_edit.pump_name = form.pump_name.data
        pump_to_edit.pump_brand = form.pump_brand.data
        pump_to_edit.pump_flow_rate = lps_to_mlpm(form.pump_flow_rate.data)
        pump_to_edit.pump_head = m_to_cm(form.pump_head.data)
        pump_to_edit.pump_watts = kw_to_w(form.pump_watts.data)


        # DB COMMANDS
        db.session.commit()

        # FLASH AND REDIRECT
        flash('''Your Pump brand: {}
                Flow rate: {} lps
                Head pressure: {} m
                Wattage: {} kW'''.format(form.pump_brand.data, form.pump_flow_rate.data, form.pump_head.data, form.pump_watts.data))
        return redirect(url_for('settings.index'))

    return render_template('pump_settings/edit_pump.html', form=form, pump_id = pump_id)


##################
# USER DELETE PUMP
##################
@pump_settings.route('/delete-pump', methods=['GET'])
@pump_settings.route('/delete-pump/<pump_id>', methods=['GET'])
@login_required
def delete_pump(pump_id = 0):

    if int(pump_id) <= 0:
        flash('Cant delete. This Pump does not exist.')
        return redirect(url_for('settings.index'))

    try:
        pump_to_del = Pump.query.filter_by(id = pump_id).first()
        db.session.delete(pump_to_del)
        db.session.commit()
        flash('You just deleted pump: {}'.format(pump_to_del.pump_name))
        return redirect(url_for('settings.index'))
    except Exception as e:
        flash('Error: ' + str(e))
        db.session.rollback()
        return render_template('settings/index.html')
    else:
        pass
    finally:
        pass


    flash('Error in delete_pump')
    return render_template('settings/index.html')
