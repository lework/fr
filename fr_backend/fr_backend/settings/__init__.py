# Python
import os
import logging
import importlib

# 多环境配置

logger = logging.getLogger('fr_backend.settings')

# by default use development
ENV_ROLE = os.getenv('APP_ENV', 'development')

logger.info("Load %s environment configuration!" % ENV_ROLE)

env_settings = importlib.import_module(f'fr_backend.settings.{ENV_ROLE}')

globals().update(vars(env_settings))

print('ENV:', ENV_ROLE)
print('settings:', env_settings.__file__)

try:
    # import local settings if present
    from .local import *  # noqa
except ImportError:
    pass
