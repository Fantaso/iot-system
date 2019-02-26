from flask import Blueprint, render_template, redirect, url_for, flash
from solarvibes import db
from solarvibes.site.forms import EmailForm, EmailAndTextForm, ContactUsForm # Wesite Forms
from solarvibes.site.models import NewsletterTable, AgrimoduleFBTable, PlatformFBTable, WorkWithUsTable, ContactUsTable

site = Blueprint(
    'site',
    __name__,
    template_folder="templates",
    static_folder="static",
)

@site.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm()
    if form.validate_on_submit():
        email = form.email.data
        agrimodulefb = NewsletterTable(email=email)
        db.session.add(agrimodulefb)
        db.session.commit()
        form = None
        flash('Thanks. We will maintain you update!')
        return redirect(url_for('site.index'))
    return render_template('site/index.html', form=form)


@site.route('/agrimodule', methods=['GET', 'POST'])
def agrimodule():
    form = EmailAndTextForm()
    if form.validate_on_submit():
        email = form.email.data
        msg = form.msg.data
        agrimodulefb = AgrimoduleFBTable(email=email, msg=msg)
        db.session.add(agrimodulefb)
        db.session.commit()
        form = None
        flash('Thanks. We definitely give a lot of thought about it!')
        return redirect(url_for('site.agrimodule'))
    return render_template('site/agrimodule.html', form=form)


@site.route('/platform', methods=['GET', 'POST'])
def platform():
    form = EmailAndTextForm()
    if form.validate_on_submit():
        email = form.email.data
        msg = form.msg.data
        platformfb = PlatformFBTable(email=email, msg=msg)
        db.session.add(platformfb)
        db.session.commit()
        form = None
        flash('Thanks. Your feedback is valuable to us!')
        return redirect(url_for('site.platform'))
    return render_template('site/platform.html', form=form)

@site.route('/about', methods=['GET', 'POST'])
def about():
    form = EmailAndTextForm()
    if form.validate_on_submit():
        email = form.email.data
        msg = form.msg.data
        workwithusus = WorkWithUsTable(email=email, msg=msg)
        db.session.add(workwithusus)
        db.session.commit()
        form = None
        flash('Thanks. Our HR department will contact you!')
        return redirect(url_for('site.about'))
    return render_template('site/about.html', form=form)


@site.route('/contact', methods=['GET', 'POST'])
def contact():
    # pre_contact = PreContactUsForm('Carlos','carlos@sv.de','+176-55858585','I would like to get a quotation for my farm 1 hectare located in Berlin')
    form = ContactUsForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        msg = form.msg.data
        newsletter = ContactUsTable(name=name, email=email, phone=phone, msg=msg)
        db.session.add(newsletter)
        db.session.commit()
        form = None
        flash('Thanks. We will get back to your shortly!')
        return redirect(url_for('site.contact'))
    return render_template('site/contact.html', form=form)
