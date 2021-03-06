from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import LazyObject
from django.utils.importlib import import_module

from filebrowser import settings

def get_storage_class(import_path=None):
    if import_path is None:
        import_path = settings.DEFAULT_FILE_STORAGE
    try:
        dot = import_path.rindex('.')
    except ValueError:
        raise ImproperlyConfigured("%s isn't a storage module." % import_path)
    module, classname = import_path[:dot], import_path[dot+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing storage module %s: "%s"' % (module, e))
    try:
        return getattr(mod, classname)
    except AttributeError:
        raise ImproperlyConfigured('Storage module "%s" does not define a "%s" class.' % (module, classname))

class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class()(location=settings.MEDIA_ROOT)
default_storage = DefaultStorage()

