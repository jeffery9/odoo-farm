from . import models
from . import wizards


def post_init_hook(cr, registry):
    from .hooks import post_init_hook as hook
    return hook(cr, registry)
