from functools import partial
from flaskext.script import Manager, Server, Shell
from werkzeug import create_environ

from coqd.runner import main as coqd_main
from cockerel.webapp import app
from cockerel.utilities import new_app
from cockerel.models import db, schema
from cockerel.auth import principals


def _make_context():
    return dict(app=new_app(app), db=db, models=schema)


manager = Manager(partial(new_app, app))
manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command("runserver", Server())
manager.add_option('--serialize',  action="store_true",
                default=False, help="Serialize output to JSON")


@manager.command
def initdb():
    # A request_context is required to use these helper functions
    with new_app(app).request_context(create_environ()):
        db.drop_all()
        db.create_all()
        readaction = schema.Action("read")
        insertaction = schema.Action("insert")
        deleteaction = schema.Action("delete")
        editaction = schema.Action("edit")
        db.session.add(readaction)
        db.session.add(insertaction)
        db.session.add(deleteaction)
        db.session.add(editaction)
        db.session.commit()


@manager.command
def initprincipal():
    principals.app = app


@manager.option('--serialize',  action="store_true",
                default=False,
                help="Serialize output to JSON")
def runcoqd(serialize):
    coqd_main()


if __name__ == "__main__":
    manager.run()
