from . import models
from . import wizards


def post_init_hook(env):
    """
    Initialize default agricultural industry packages after module installation.
    """
    env['agri.industry.data.package'].create_default_packages()
