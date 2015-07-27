from django.conf import settings

BACKEND = getattr(settings, 'CONSTANCE_BACKEND',
                  'constance.backends.redisd.RedisBackend')

APP_NAME = getattr(settings, 'CONSTANCE_APP_NAME',
                  'constance')

OBJECT_NAME = getattr(settings, 'CONSTANCE_OBJECT_NAME',
                  'config')

CONFIG = getattr(settings, 'CONSTANCE_CONFIG', {})

ADDITIONAL_FIELDS = getattr(settings, 'CONSTANCE_ADDITIONAL_FIELDS', {})

DATABASE_CACHE_BACKEND = getattr(settings, 'CONSTANCE_DATABASE_CACHE_BACKEND',
                                 None)

DATABASE_CACHE_AUTOFILL_TIMEOUT = getattr(settings,
                                          'CONSTANCE_DATABASE_CACHE_AUTOFILL_TIMEOUT',
                                          60 * 60 * 24)

DATABASE_PREFIX = getattr(settings, 'CONSTANCE_DATABASE_PREFIX', '')

REDIS_PREFIX = getattr(settings, 'CONSTANCE_REDIS_PREFIX', 'constance:')

REDIS_CONNECTION_CLASS = getattr(settings, 'CONSTANCE_REDIS_CONNECTION_CLASS',
                                 None)

REDIS_CONNECTION = getattr(settings, 'CONSTANCE_REDIS_CONNECTION', {})

SUPERUSER_ONLY = getattr(settings, 'CONSTANCE_SUPERUSER_ONLY', True)

EMAIL_VALUES_SEPARATOR = getattr(settings, 'CONSTANCE_EMAIL_VALUES_SEPARATOR', ',')
