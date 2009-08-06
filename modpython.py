from os.path import dirname, isfile

ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"

class ModPythonBuildoutHandler(object):
    """
    Try to locate and execute buildouts bin/django to set up the environment before calling django.core.handlers.modpython.handler
    """

    def __call__(self, req):
        if ENVIRONMENT_VARIABLE in req.subprocess_env:
            settings_module = req.subprocess_env[ENVIRONMENT_VARIABLE]

            try:
                mod = __import__(settings_module, {}, {}, [''])
            except ImportError, e:
                raise ImportError, "Could not import settings '%s' (Is it on sys.path? Does it have syntax errors?): %s" % (settings_module, e)

            activate_this = '%s/bin/django' % dirname(dirname(mod.__file__))

            if isfile(activate_this): 
                execfile(activate_this, dict(__file__=activate_this))

        from django.core.handlers import modpython
        return modpython.handler(req)


def handler(req):
    return ModPythonBuildoutHandler()(req)

