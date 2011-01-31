from flaskext.principal import Principal
from util import login_required, permissions

principals = Principal()

__all__ = ['principals']