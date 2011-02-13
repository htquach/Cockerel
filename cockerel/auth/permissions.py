"""
Permissions
===========

Will specify what roles or attributes are needed to be held by an Identity for
it to access a resource. The resource can be anything within the application.
However, it should be restricted to page endpoints. Privileges which will be
integrated later will restrict the access to data in a more fine grained manner

"""

from flask import g
from flaskext.principal import (
    identity_loaded,
    Permission,
    ActionNeed)

from cockerel.models.schema import User


def permission(*roles):
    perm = Permission(ActionNeed('none'))
    for x in roles:
        perm = perm.union(x)
    return perm


class Permissions(dict):
    def __getattr__(self, attr):
        try:
            return self[attr]
        except:
            return super(self, dict).attr

    def __setattr__(self, attr, value):
        self[attr] = value

permissions = Permissions()

read_action = Permission(ActionNeed('read'))
insert_action = Permission(ActionNeed('insert'))
edit_action = Permission(ActionNeed('edit'))
delete_action = Permission(ActionNeed('delete'))
full_access_action = permission(read_action, insert_action,
                                     edit_action, delete_action)


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    print ("This identity is: " + identity.name)
    user = User.query.filter_by(
                username=identity.name).first()
    # Update the roles that a user can provide
    for action in user.actions:
        identity.provides.add(ActionNeed(action.actionname))
    print (identity.provides)
    g.identity = identity
    g.identity.user = user
