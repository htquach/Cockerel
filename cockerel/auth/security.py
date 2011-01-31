"""
Security
========

Inflate and set the users Identity. Works with `permission.Permissions` since
all roles will be added to an Identity and then checked before routing.
"""

import hashlib

from flask import g, session
from flaskext.principal import Identity

from cockerel.auth import principals
from cockerel.models.schema import User


def check_user():
    g.identity = Identity(User.query.filter_by(
        username=session.get('username')))


@principals.identity_saver
def set_user(identity):
    g.identity = identity
    session['username'] = identity.username


def get_activationcode(user):
    return hashlib.sha1(user.username.lower() +
                        user.email.lower()).hexdigest()