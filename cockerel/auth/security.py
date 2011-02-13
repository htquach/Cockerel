"""
Security
========

Inflate and set the users Identity. Works with `permission.Permissions` since
all roles will be added to an Identity and then checked before routing.
"""

import hashlib

from flask import app, g, session
from flaskext.principal import Identity, identity_loaded

from cockerel.auth import principals
from cockerel.models.schema import User


@principals.identity_loader
def load_identity():
    g.user = None
    if session.get('identity'):
        user = User.query.filter_by(
                username=session.get('identity').username).first()
        if user:
            g.identity = Identity(user.username)
            g.user = user
            identity_loaded.send(app, identity=g.identity)
    if g.user:
        print("Loaded: " + g.user.username)
    else:
        print("Loaded: None")


@principals.identity_saver
def save_identity(identity):
    session['identity'] = identity


def get_activationcode(user):
    return hashlib.sha1(user.username.lower() +
                        user.email.lower()).hexdigest()