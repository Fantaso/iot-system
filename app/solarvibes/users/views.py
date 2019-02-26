from flask import Blueprint, render_template, redirect, url_for, flash
from solarvibes import db, photos
from solarvibes.users.forms import UserProfileForm, PreUserProfileForm # User Forms
from solarvibes.models import User
from flask_login import current_user
from flask_security import login_required

users = Blueprint(
    'users',
    __name__,
    template_folder="templates",
)

##################
# USER PROFILE
##################
@users.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    name = current_user.name
    return render_template('users/profile.html', name=name)

##################
# USER PROFILE EDIT
##################
@users.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.filter_by(email=current_user.email).first()
    # Prepopulate form
    myUser = PreUserProfileForm(username = user.username,
                                name = user.name,
                                last_name = user.last_name,
                                address = user.address,
                                zipcode = user.zipcode,
                                city = user.city,
                                state = user.state,
                                country = user.country,
                                email = user.email,
                                email_rec = user.email_rec,
                                birthday = user.birthday,
                                image = user.image,
                                mobile = user.mobile)
    form = UserProfileForm(obj=myUser)
    # if image is not uploaded it gets a TypeError
    if form.validate_on_submit():   # IF request.methiod == 'POST'
        user = User.query.filter_by(id=current_user.get_id()).first()
        # FIELD OBJS  TO DB
        try:
            # IMAGE HANDLING
            if not form.image.data == user.image:
                image_filename = photos.save(form.image.data)
                image_url = photos.url(image_filename)
                user.image = image_url
            # REST OF FORM HANDLING
            user.username = form.username.data
            user.name = form.name.data
            user.last_name = form.last_name.data
            user.address = form.address.data
            user.zipcode = form.zipcode.data
            user.city = form.city.data
            user.state = form.state.data
            user.country = form.country.data
            user.email = form.email.data
            user.email_rec = form.email_rec.data
            user.birthday = form.birthday.data
            user.mobile = form.mobile.data
            db.session.commit()
        except Exception as e:
            flash(e)
            print(e)
            db.session.rollback()
        flash('You updated sucessfully your profile')
        return redirect(url_for('users.profile'))
    return render_template('users/edit_profile.html', form=form)
