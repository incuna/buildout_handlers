from os.path import dirname, isfile
import imp

ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"

class ModPythonBuildoutHandler(object):
    """
    Try to locate and execute buildouts bin/django to set up the environment before calling django.core.handlers.modpython.handler
    """

    def __call__(self, req):
        if ENVIRONMENT_VARIABLE in req.subprocess_env:
            settings_module = req.subprocess_env[ENVIRONMENT_VARIABLE]
           
            settings_parent_list = settings_module.split(".")
            settings_parent = ".".join(settings_parent_list[:-1])

            try:
                pth2 = imp.find_module(settings_parent)[1]
            except ImportError, e:
                raise ImportError, "Could not import settings '%s' (Is it on sys.path? Does it have syntax errors?): %s" % (settings_module, e)

            activate_this = '%s/bin/django' % dirname(pth2)

            if isfile(activate_this): 
                execfile(activate_this, dict(__file__=activate_this))

        from django.core.handlers import modpython
        return modpython.handler(req)


def handler(req):
    return ModPythonBuildoutHandler()(req)

