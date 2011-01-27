import hashlib
import smtplib

from flask import (
    g,
    Module,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flatland.out.markup import Generator

#TODO: import cockerel.auth.security does not work.
#from cockerel.auth.security import get_activationcode
from cockerel.models.schema import db, User
from cockerel.forms import LoginForm, SignupForm, ActivateLoginForm

admin = Module(__name__)


@admin.route('/login', methods=['GET', 'POST'])
def login():
    # TODO: make this do better auth, it needs to set a cookie for a period of
    #  time
    gen = Generator()
    if request.method == 'POST':
        form = LoginForm.from_flat(request.form)
        if form.validate():
            user = User.query.filter_by(
                username=request.form['username']).first()
            if user != None:
                if not user.activestatus:
                    form.add_error(
                        """Username %s need to be activated before 1st login.
                        It can only be activated with the link sent to email of this username.""" %
                        form['username'].value)
                    return render_template("admin/login.html", form=form, html=gen)
                if user.check_password(request.form['password']):
                    g.user = user
                    set_user()
                    if request.args:
                        return redirect(request.args.get('next'))
                    else:
                        return redirect(url_for('frontend.index'))
            form.add_error('Invalid username %s or password.' % form['username'].value)
            return render_template("admin/login.html", form=form, html=gen)
        else:
            return render_template("admin/login.html", form=form, html=gen)
    form = LoginForm()
    return render_template("admin/login.html",
                           form=form,
                           html=gen,
                           **request.args)


@admin.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('frontend.index'))


@admin.route('/signup', methods=['GET', 'POST'])
def signup():
    gen = Generator()
    if request.method == 'POST':
        form = SignupForm.from_flat(request.form)
        if form.validate():
            existingUser = User.query.filter_by(
                username=request.form['username']).first()
            if existingUser != None:
                form['username'].add_error(
                    'Username %s is taken' % form['username'].value)
                gen = Generator()
                return render_template("admin/signup.html", form=form, html=gen)
            existingEmail = User.query.filter_by(
                email=request.form['email']).first()
            if existingEmail != None:
                form['email'].add_error(
                    'There is an account associated with %s.' % form['email'].value)
                gen = Generator()
                return render_template("admin/signup.html", form=form, html=gen)
            user = User(request.form['username'],
                       request.form['password'],
                       request.form['email'],
                       request.form['firstname'],
                       request.form['lastname'],
                       False)
            db.session.add(user)
            db.session.commit()
            #TODO work around since SMTP mail server is not setup.
            form = SignupForm()
            form.add_error(send_activationcode(user))
            return render_template("admin/signup.html",
                                   form=form,
                                   html=gen)
        else:
            return render_template("admin/signup.html", 
                                   form=form, 
                                   html=gen)
    form = SignupForm()
    return render_template("admin/signup.html",
                           form=form,
                           html=gen)

@admin.route('/activatelogin', methods=['GET', 'POST'])
def activatelogin():
    gen = Generator()
    if request.method == 'POST':
        form = ActivateLoginForm.from_flat(request.form)
        if form.validate():
            user = User.query.filter_by(
                username=request.form['username']).first()
            if user == None:
                form['username'].add_error(
                    'Username %s is invalid' % form['username'].value)
                return render_template("admin/activatelogin.html", form=form, html=gen)
            if get_activationcode(user) != request.args['activationcode']:
                form.add_error(
                    'incorrect user name or invalid activation code %s.' %
                    request.args['activationcode'])
                return render_template("admin/activatelogin.html",
                                       form=form,
                                       html=gen)
            user.activestatus = True
            db.session.commit()
            form = LoginForm()
            return render_template("admin/login.html",
                                   form=form,
                                   html=gen)
        else:
            return render_template("admin/activatelogin.html",
                                   form=form,
                                   html=gen)
    form = ActivateLoginForm()
    return render_template("admin/activatelogin.html",
                           form=form,
                           html=gen)

def send_activationcode(user):
    sender = 'Cockerel@Cockerel.com'
    receivers = user.email
    activationURL = "http://127.0.0.1:5000" +\
                    url_for('activatelogin',
                            activationcode=get_activationcode(user))
    message = """From: Cockerel <%s>
    To: %s %s <%s>
    Subject: Welcome to Cockerel

    Hi %s,

    Your username is %s.  Please use this link to activate your account %s.

    Thank you,
    Cockerel
    """ % (sender,
           user.firstname,
           user.lastname,
           receivers,
           user.firstname,
           user.username,
           activationURL)
    return sender, receivers, message
#    TODO: Supply SMTP server information to use the email feature
#    try:
#       smtpObj = smtplib.SMTP('localhost')
#       smtpObj.sendmail(sender, receivers, message)
#       return True
#    except smtplib.SMTPException:
#       return False

def get_activationcode(user):
    return hashlib.sha1(user.username.lower() +
                        user.email.lower()).hexdigest()

def check_user():
    g.user = User.query.filter_by(
        username=session.get('username')).first()


def set_user():
    session['username'] = g.user.username


admin.before_app_request(check_user)
