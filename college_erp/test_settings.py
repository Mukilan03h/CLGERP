from .settings import *
import mongoengine

mongoengine.disconnect()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
